from django.db import models


class uploadFile(models.Model):
    path     = models.CharField(max_length=4096)
    pub_date = models.DateTimeField('date uploaded')
    name     = models.CharField(max_length=255)
