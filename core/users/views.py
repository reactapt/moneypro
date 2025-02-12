from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.models import EmployeeProfile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

@login_required
def link_telegram(request):
    if request.method == "POST":
        telegram_id = request.POST.get("telegram_id")
        employee = EmployeeProfile.objects.get(user=request.user)
        employee.telegram_id = telegram_id
        employee.save()
        return redirect("profile")
    return render(request, "users/link_telegram.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})