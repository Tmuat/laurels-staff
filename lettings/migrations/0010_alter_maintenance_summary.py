# Generated by Django 3.2.4 on 2021-09-20 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lettings", "0009_alter_maintenance_contractor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maintenance",
            name="summary",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]