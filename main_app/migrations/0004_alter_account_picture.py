# Generated by Django 4.0.3 on 2022-04-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_account_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.CharField(blank=True, default='https://i.imgur.com/VKXouC4.png', max_length=2000, null=True),
        ),
    ]