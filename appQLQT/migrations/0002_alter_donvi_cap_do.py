# Generated by Django 4.2.11 on 2024-11-23 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appQLQT', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donvi',
            name='cap_do',
            field=models.CharField(choices=[('tong', 'Đơn vị'), ('trung_doan', 'Trung đoàn'), ('dai_doi', 'Đại đội'), ('tieu_doi', 'Tiểu đội'), ('hau_can', 'Hậu cần')], max_length=20),
        ),
    ]
