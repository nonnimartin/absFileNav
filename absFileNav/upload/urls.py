from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path/', views.new_path, name='new_path'),
    path('user_settings', views.user_settings, name='user_settings'),
    path('view_files', views.view_files, name='view_files'),
]