<<<<<<< HEAD
# Generated by Django 4.0.3 on 2022-04-04 14:23
=======
# Generated by Django 4.0.3 on 2022-04-04 14:34
>>>>>>> main

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('model', models.FileField(blank=True, default='models/2022/04/$D/Earth.glb', null=True, upload_to='models/%Y/%m/$D/')),
                ('text_content', models.TextField(blank=True, default=None, max_length=1000, null=True)),
                ('tags', models.TextField(blank=True, default=None, max_length=1000, null=True)),
                ('downloads', models.IntegerField(default=0)),
                ('type', models.CharField(default='STL', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('text_content', models.CharField(max_length=3000)),
                ('title', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main_app.post')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(blank=True, default='https://i.imgur.com/VKXouC4.png', max_length=2000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
