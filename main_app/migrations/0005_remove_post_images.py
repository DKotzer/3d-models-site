# Generated by Django 4.0.3 on 2022-04-03 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_photo_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
    ]