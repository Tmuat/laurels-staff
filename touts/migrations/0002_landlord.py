# Generated by Django 3.2.5 on 2021-12-01 07:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('landlord_name', models.CharField(max_length=150)),
                ('address_line_1', models.CharField(max_length=150)),
                ('address_line_2', models.CharField(blank=True, max_length=150, null=True)),
                ('town', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'Tout Landlord',
                'verbose_name_plural': 'Tout Landlords',
                'ordering': ['postcode', 'address_line_1', 'landlord_name'],
                'unique_together': {('postcode', 'address_line_1', 'address_line_2')},
            },
        ),
    ]
