from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import WorkTime

@login_required
@user_passes_test(lambda u: u.profile.role == 'accountant')
def work_time_list(request):
    work_times = WorkTime.objects.filter(status='pending')
    return render(request, 'time_tracking/list.html', {'work_times': work_times})