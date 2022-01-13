from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test_view),
    path('generic', views.generic),
    path('add_controller', views.add_controller),
    path('get_available_controllers', views.get_available_controllers),
    path('get_data_as_csv', views.get_data_as_csv),
    path('target', views.target_parameter),
    path('home', views.home),
]