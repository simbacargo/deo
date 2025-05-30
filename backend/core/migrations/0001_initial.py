# Generated by Django 5.0.4 on 2024-06-07 12:47

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('uid', models.CharField(default=core.models.get_token, editable=False, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('caption', models.CharField(blank=True, max_length=80, null=True)),
                ('product_id', models.CharField(blank=True, max_length=80, null=True)),
                ('file', models.FileField(upload_to='images/%Y/%m/%d/')),
                ('file_base64', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Video_Description', models.CharField(blank=True, max_length=500, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('videofile', models.FileField(null=True, upload_to='deploy/videos/%Y/%m/%d/', verbose_name='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ViewHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('product', models.CharField(max_length=150)),
                ('date_joineds', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
