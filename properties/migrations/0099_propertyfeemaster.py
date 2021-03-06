# Generated by Django 3.2.11 on 2022-02-07 19:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0098_offer_waiting_on_chain'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyFeeMaster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('fee', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('new_business', models.FloatField(blank=True, null=True)),
                ('propertyprocess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_fees_master', to='properties.propertyprocess')),
            ],
            options={
                'verbose_name': 'Property Fee Master',
                'verbose_name_plural': 'Property Fees Master',
                'ordering': ['propertyprocess__property__postcode', 'propertyprocess__property__address_line_1', '-created'],
            },
        ),
    ]
