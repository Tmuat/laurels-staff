# Generated by Django 3.2.5 on 2021-12-18 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0022_alter_toutproperty_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landlord',
            name='county',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
