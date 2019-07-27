from django.urls import path
from django.conf.urls import url
import absFileNav.settings  as settings

from . import views

# import chunked_upload classes
from .chunked_upload import (
    ChunkedUploadDemo, MyChunkedUploadView, MyChunkedUploadCompleteView
)

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path/', views.new_path, name='new_path'),
    path('user_settings', views.user_settings, name='user_settings'),
    url(r'^/?$',
        ChunkedUploadDemo.as_view(), name='chunked_upload'),
    url(r'^api/chunked_upload/?$',
        MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    url(r'^api/chunked_upload_complete/?$',
        MyChunkedUploadCompleteView.as_view(),
        name='api_chunked_upload_complete'),
    # url(r'^static/(.*)$',
    #     'django.views.static.serve',
    #     {'document_root': settings.STATIC_ROOT, 'show_indexes': False}),
]