# Generated by Django 4.0.3 on 2022-04-02 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_remove_photo_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.post'),
            preserve_default=False,
        ),
    ]