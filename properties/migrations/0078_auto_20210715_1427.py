# Generated by Django 3.2.4 on 2021-07-15 13:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0077_propertyprocess_reduction_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyprocess',
            name='reduction_count',
        ),
        migrations.CreateModel(
            name='Reduction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField()),
                ('price_change', models.PositiveIntegerField()),
                ('propertyprocess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reduction', to='properties.propertyprocess')),
            ],
            options={
                'verbose_name': 'Reduction',
                'verbose_name_plural': 'Reductions',
                'ordering': ['propertyprocess__property__postcode', 'propertyprocess__property__address_line_1', '-created'],
            },
        ),
    ]
