# Generated by Django 4.2.11 on 2024-11-28 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appQLQT', '0004_donvi_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cap_do', models.CharField(blank=True, choices=[('tong', 'Kho'), ('tieu_doan', 'Tiểu đoàn'), ('trung_doi', 'Trung đội'), ('dai_doi', 'Đại đội')], max_length=20, null=True)),
                ('ngay_sinh', models.DateField(blank=True, null=True)),
                ('so_dien_thoai', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]