# Generated by Django 2.2.1 on 2019-06-07 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_delete_queuedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_folder', models.CharField(max_length=4096)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('show_files', models.BooleanField(default=False)),
            ],
        ),
    ]
