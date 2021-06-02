# Generated by Django 3.2 on 2021-06-02 11:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0033_salestatusphase'),
    ]

    operations = [
        migrations.AddField(
            model_name='salestatusphase',
            name='overall_phase',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)]),
        ),
    ]