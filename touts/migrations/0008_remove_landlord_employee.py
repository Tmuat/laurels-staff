# Generated by Django 3.2.5 on 2021-12-05 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0007_auto_20211205_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landlord',
            name='employee',
        ),
    ]
