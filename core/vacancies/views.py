from django.shortcuts import render
from .models import Vacancy

def vacancy_list(request):
    vacancies = Vacancy.objects.filter(status='open')
    return render(request, 'vacancies/list.html', {'vacancies': vacancies})