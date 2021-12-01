# Generated by Django 3.2.5 on 2021-12-01 07:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToutProperty',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('address_line_1', models.CharField(max_length=150)),
                ('address_line_2', models.CharField(blank=True, max_length=150, null=True)),
                ('town', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'Tout Property',
                'verbose_name_plural': 'Tout Properties',
                'ordering': ['postcode', 'address_line_1'],
                'unique_together': {('postcode', 'address_line_1', 'address_line_2')},
            },
        ),
    ]
