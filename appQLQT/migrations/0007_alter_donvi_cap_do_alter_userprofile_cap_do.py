# Generated by Django 4.2.11 on 2024-11-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appQLQT', '0006_remove_userprofile_ngay_sinh_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donvi',
            name='cap_do',
            field=models.CharField(choices=[('tong', 'Kho'), ('tieu_doan', 'Tiểu đoàn'), ('dai_doi', 'Đại đội'), ('trung_doi', 'Trung đội')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cap_do',
            field=models.CharField(blank=True, choices=[('tong', 'Kho'), ('tieu_doan', 'Tiểu đoàn'), ('dai_doi', 'Đại đội'), ('trung_doi', 'Trung đội')], max_length=20, null=True),
        ),
    ]
