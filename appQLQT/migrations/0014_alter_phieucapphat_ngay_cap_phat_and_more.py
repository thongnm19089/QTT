# Generated by Django 4.2.11 on 2024-11-29 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appQLQT', '0013_alter_quantutrang_ma_qtt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phieucapphat',
            name='ngay_cap_phat',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='phieunhan',
            name='ngay_nhan',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='phieunhap',
            name='ngay_nhap',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='phieuxuat',
            name='ngay_xuat',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]