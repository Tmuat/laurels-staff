# Generated by Django 3.2.4 on 2021-08-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0089_auto_20210811_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealextralettings',
            name='term',
            field=models.IntegerField(choices=[(6, '6 Months'), (12, '12 Months'), (18, '18 Months'), (24, '24 Months'), (36, '36 Months')], null=True),
        ),
    ]
