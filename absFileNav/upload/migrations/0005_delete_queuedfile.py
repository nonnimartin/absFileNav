# Generated by Django 2.2.1 on 2019-06-02 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_queuedfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='QueuedFile',
        ),
    ]
