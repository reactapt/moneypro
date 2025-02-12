from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('guest', 'Гость'),
        ('employee', 'Сотрудник'),
        ('accountant', 'Бухгалтер'),
        ('admin', 'Админ'),
    ], default='guest')

class EmployeeProfile(models.Model):
    user = models.OneToOneField(AbstractUser, on_delete=models.CASCADE, related_name='profile')
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)  # ID Telegram

    def __str__(self):
        return f"{self.user.username} ({self.position})"

class WorkTime(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='work_times')
    start_time = models.DateTimeField(null=True, blank=True)  # Начало рабочего дня
    end_time = models.DateTimeField(null=True, blank=True)   # Конец рабочего дня
    screenshots = models.TextField(blank=True, null=True)    # Ссылки на скриншоты
    status = models.CharField(max_length=20, choices=[('pending', 'На рассмотрении'), ('approved', 'Подтверждено')], default='pending')

    def duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"{self.employee.user.username} - {self.start_time}"