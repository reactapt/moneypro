from django.db import models
from users.models import EmployeeProfile

class WorkTime(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='work_times')
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=20, choices=[('work', 'Рабочий день'), ('vacation', 'Отпуск'), ('sick', 'Больничный')])
    status = models.CharField(max_length=20, choices=[('approved', 'Подтверждено'), ('pending', 'На рассмотрении')], default='pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"