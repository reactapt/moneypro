import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from users.models import EmployeeProfile, WorkTime
from django.utils import timezone

# Токен вашего бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Используй /start_day для начала рабочего дня и /stop_day для завершения.")

def start_day(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        employee = EmployeeProfile.objects.get(telegram_id=user_id)
        # Создаем запись о начале рабочего дня
        WorkTime.objects.create(employee=employee, start_time=timezone.now())
        update.message.reply_text("Рабочий день начат!")
    except EmployeeProfile.DoesNotExist:
        update.message.reply_text("Вы не привязаны к системе. Обратитесь к администратору.")

def stop_day(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        employee = EmployeeProfile.objects.get(telegram_id=user_id)
        # Находим последнюю запись о рабочем времени
        work_time = WorkTime.objects.filter(employee=employee, end_time__isnull=True).last()
        if work_time:
            work_time.end_time = timezone.now()
            work_time.save()
            duration = work_time.duration()
            update.message.reply_text(f"Рабочий день завершен! Продолжительность: {duration}")
        else:
            update.message.reply_text("Не найдена запись о начале рабочего дня.")
    except EmployeeProfile.DoesNotExist:
        update.message.reply_text("Вы не привязаны к системе. Обратитесь к администратору.")

def handle_screenshot(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        employee = EmployeeProfile.objects.get(telegram_id=user_id)
        work_time = WorkTime.objects.filter(employee=employee, end_time__isnull=False).last()
        if work_time:
            # Сохраняем ссылку на скриншот
            file = update.message.photo[-1].get_file()
            screenshot_url = file.file_path
            work_time.screenshots = screenshot_url
            work_time.save()
            update.message.reply_text("Скриншот сохранен и отправлен бухгалтеру.")
        else:
            update.message.reply_text("Сначала завершите рабочий день с помощью /stop_day.")
    except EmployeeProfile.DoesNotExist:
        update.message.reply_text("Вы не привязаны к системе. Обратитесь к администратору.")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("start_day", start_day))
    dispatcher.add_handler(CommandHandler("stop_day", stop_day))

    # Обработчик скриншотов
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_screenshot))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()