# Generated by Django 3.2.4 on 2021-07-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0076_auto_20210709_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyprocess',
            name='reduction_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]