from django.urls import path
from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path/', views.new_path, name='new_path'),
]