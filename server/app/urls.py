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
    path('remove_target', views.remove_target),
    path('all_targets', views.all_targets),
    path('report_device', views.report_device),
    path('datastring', views.post_with_datastring),
    path('csv', views.post_as_csv),
    path('controller_has_data', views.controller_has_data),
    path('db', views.db_testing),
    path('home', views.home),
    path('hourly_average', views.hourly_average),
    path('get_averages_as_csv', views.get_averages_as_csv),
    path('control_systems_activity', views.control_system_activity),
]