from django.urls import path
from django.conf.urls import url
from .views import (ChunkedUploadView, ChunkedUploadCompleteView)

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path/', views.new_path, name='new_path'),
    path('user_settings', views.user_settings, name='user_settings'),
    url(r'^chunked_upload/?$', ChunkedUploadView.as_view(), name='chunked_upload'),
    url(r'^chunked_upload_complete/?$', ChunkedUploadCompleteView.as_view(), name='chunked_upload_complete'),
]