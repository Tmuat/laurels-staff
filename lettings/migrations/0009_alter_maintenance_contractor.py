# Generated by Django 3.2.4 on 2021-09-16 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lettings", "0008_alter_maintenance_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maintenance",
            name="contractor",
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
