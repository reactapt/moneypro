from django.db import models
from users.models import EmployeeProfile

class Salary(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='salaries')
    period = models.DateField()  # Период (месяц/год)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('paid', 'Выплачено'), ('pending', 'Ожидает')], default='pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.period}"