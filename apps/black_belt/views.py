# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from ..login_registration.models import User
from .models import Appointment
from django.contrib import messages
import datetime
from time import gmtime, strftime, strptime

# Create your views here.
def appointments(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id = request.session["user"]),
        'time' : strftime("%B %d, %Y", gmtime()),
        'appointments' : User.objects.get(id = request.session["user"]).appointments.all(),
        'today' : datetime.datetime.today(),
        'tomorrow' : datetime.date.today() + datetime.timedelta(days=1),
        }
    #context["tomorrow"] = strftime("%B %d, %Y", gmtime())
    return render(request, 'black_belt/appointments.html', context)

def Add(request):
    if "user" not in request.session:
        return redirect('/')
    curUser = request.session["user"]
    response = Appointment.objects.appointment_validator(request.POST, curUser)
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val)
        return redirect('/black_belt/appointments')
    return redirect('/black_belt/appointments')

def Edit(request, number):
    if "user" not in request.session:
        return redirect('/')
    time = Appointment.objects.get(id = number).time
    time =  time.strftime('%H:%M')
    context = {
        "appointment" : Appointment.objects.get(id = number),
        "time" : time
        }
    return render(request, 'black_belt/edit.html', context)

def EditValidation(request, number):
    if "user" not in request.session:
        return redirect('/')
    curUser = request.session["user"]
    response = Appointment.objects.appointment_edit_validator(request.POST, number)
    print response, "**********8"
    if response["status"] == False:
        for val in response["errors"]:
            messages.error(request, val)
        return redirect('/black_belt/appointments/{}'.format(number))
    return redirect('/black_belt/appointments')

def logOut(request):
    request.session.clear()
    return redirect('/')

def remove(request, number):
    Appointment.objects.get(id = number).delete()
    return redirect('/black_belt/appointments')
