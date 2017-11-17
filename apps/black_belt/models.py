# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User
import datetime
from time import gmtime, strftime, strptime

# Create your models here.
class AppointmentManager(models.Manager):
    def appointment_validator(self, postData ,userId):
        response = {
            'status' : True,
            'errors' : []
            }
        if len(postData['date']) and len(postData["time"]) and len(postData["task"]) > 0:
            userDate = datetime.datetime.strptime(postData["date"],'%Y-%m-%d')
            userTime = datetime.datetime.strptime(postData["time"], '%H:%M')
            if userDate < datetime.datetime.today():
                response["errors"].append("Date must be at a future time!")
        else:
            response["errors"].append("All fields must be entered!")
        if len(response["errors"]) == 0:
            curUser = User.objects.get(id=userId)
            message = Appointment.objects.create(date = userDate, time = userTime, task = postData["task"], user = curUser, status = 0)
        else:
            response["status"] = False
        return response
    def appointment_edit_validator(self, postData, number):
        response = {
            'status' : True,
            'errors' : []
            }
        if len(postData['date']) and len(postData["time"]) and len(postData["task"]) > 0:
            userDate = datetime.datetime.strptime(postData["date"],'%Y-%m-%d')
            userTime = datetime.datetime.strptime(postData["time"], '%H:%M')
            if userDate < datetime.datetime.today():
                response["errors"].append("Date must be at a future time!")
        else:
            response["errors"].append("All fields must be entered!")
        appointment = self.get(id = number)
        if postData["status"] == "Done":
            statusUp = 1
        elif postData["status"] == "Missed":
            statusUp = 2
        else:
            statusUp = 0
        if len(response["errors"]) == 0:
            if postData["task"] != appointment.task or statusUp != appointment.status:
                appointment.status = statusUp
                appointment.task = postData["task"]
                appointment.time = userTime
                appointment.date = userDate
                appointment.save()
        else:
            response["status"] = False
        return response

class Appointment(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    task = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='appointments')
    status= models.IntegerField()
    objects = AppointmentManager()
