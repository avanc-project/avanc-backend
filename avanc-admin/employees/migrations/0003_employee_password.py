# Generated by Django 4.2.11 on 2024-12-18 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0002_alter_salaryadvancerequest_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="password",
            field=models.CharField(
                default="defaultpassword", max_length=128, verbose_name="password"
            ),
        ),
    ]
