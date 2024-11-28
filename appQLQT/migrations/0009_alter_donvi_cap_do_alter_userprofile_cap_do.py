# Generated by Django 4.2.11 on 2024-11-28 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appQLQT', '0008_userprofile_don_vi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donvi',
            name='cap_do',
            field=models.CharField(choices=[('kho', 'Kho'), ('tieu_doan', 'Tiểu đoàn'), ('dai_doi', 'Đại đội'), ('trung_doi', 'Trung đội')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cap_do',
            field=models.CharField(blank=True, choices=[('kho', 'Kho'), ('tieu_doan', 'Tiểu đoàn'), ('dai_doi', 'Đại đội'), ('trung_doi', 'Trung đội')], max_length=20, null=True),
        ),
    ]