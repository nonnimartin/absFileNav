from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_path', views.new_path, name='new_path'),
    path('user_settings', views.user_settings, name='user_settings'),
    path('clear_base_folder', views.clear_base_folder, name='clear_base_folder'),
    path('receive_resumable', views.receive_resumable, name='receive_resumable'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)