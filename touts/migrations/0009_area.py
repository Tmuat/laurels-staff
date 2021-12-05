# Generated by Django 3.2.5 on 2021-12-05 11:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0008_remove_landlord_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('postcode', models.CharField(max_length=8, unique=True)),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'ordering': ['postcode'],
            },
        ),
    ]
