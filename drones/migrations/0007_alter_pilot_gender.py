# Generated by Django 5.1.4 on 2024-12-30 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drones", "0006_alter_pilot_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pilot",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female")], default="M", max_length=2
            ),
        ),
    ]
