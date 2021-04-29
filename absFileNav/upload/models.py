from django.db import models


class uploadFile(models.Model):
    path = models.CharField(max_length=4096)
    pub_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    checksum = models.CharField(max_length=32)


class UserSettings(models.Model):
    base_folder = models.CharField(max_length=4096)
    last_modified = models.DateTimeField(auto_now_add=True)
    show_files = models.BooleanField(default=False)
