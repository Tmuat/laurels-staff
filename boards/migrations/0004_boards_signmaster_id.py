# Generated by Django 3.2.10 on 2022-01-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_boards_created_on_signmaster'),
    ]

    operations = [
        migrations.AddField(
            model_name='boards',
            name='signmaster_id',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True),
        ),
    ]
