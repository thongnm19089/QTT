# Generated by Django 4.2.11 on 2024-11-28 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appQLQT', '0005_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='ngay_sinh',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='so_dien_thoai',
        ),
    ]
