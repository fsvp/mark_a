from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import date
from .models import Attendance
import calendar


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('calendar')

        else:

            return render(
                request,
                'login.html',
                {'error': 'Invalid username or password'}
            )

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def calendar_view(request):

    attendance = Attendance.objects.filter(
        user=request.user
    )

    attendance_data = {}

    for item in attendance:
        attendance_data[str(item.date)] = item.status

    return render(request, 'calender.html', {
        'attendance_data': attendance_data,
    })


@login_required
def save_attendance(request):

    if request.method == "POST":

        attendance_date = request.POST.get('date')
        status = request.POST.get('status')

        if status == "empty":

            Attendance.objects.filter(
                user=request.user,
                date=attendance_date
            ).delete()

        else:

            Attendance.objects.update_or_create(
                user=request.user,
                date=attendance_date,
                defaults={
                    'status': status
                }
            )

        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False
    })