from django.db import models

class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('open', 'Открыта'), ('closed', 'Закрыта')], default='open')

    def __str__(self):
        return self.title