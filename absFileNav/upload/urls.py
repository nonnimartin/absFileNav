from django.urls import path
from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path/', views.new_path, name='new_path'),
    path('user_settings', views.user_settings, name='user_settings'),
    path('chunked_upload', views.ChunkedUploadView, name='chunked_upload'),
]