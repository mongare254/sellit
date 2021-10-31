from django.contrib import admin
from django.urls import path
from . import views

app_name='myadmin'
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('adduser', views.adduser, name='adduser'),
    path('additem', views.additem, name='additem')
]