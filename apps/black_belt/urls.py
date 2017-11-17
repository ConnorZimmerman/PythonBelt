#BLACK_BELT URL
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add_appointment', views.Add),
    url(r'edit/appointments/(?P<number>\d+)', views.EditValidation),
    url(r'appointments/(?P<number>\d+)$', views.Edit),
    url(r'^appointments$', views.appointments),
    url(r'remove/(?P<number>\d+)$', views.remove),
    url(r'logOut', views.logOut),
    url(r'^', views.appointments),
   ]