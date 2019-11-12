from django.urls import path
from django.conf.urls import url
from django.conf.urls import include

from . import views
from upload.views import (MyChunkedUploadCompleteView, ChunkedUploadDemo, MyChunkedUploadView)

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path', views.new_path, name='new_path'),
    path('chunked_view', MyChunkedUploadView.as_view(), name='chunked_view'),
    path('chunked_complete', MyChunkedUploadCompleteView.as_view(), name='chunked_complete'),
    path('user_settings', views.user_settings, name='user_settings'),
    path('clear_base_folder', views.clear_base_folder, name='clear_base_folder'),
]