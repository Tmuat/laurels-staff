# Generated by Django 3.2.5 on 2021-12-13 20:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0017_alter_toutproperty_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=100)),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('property_type', models.CharField(choices=[('House', (('house_terraced', 'House - Terraced'), ('house_end_terrace', 'House - End of Terrace'), ('house_semi_detached', 'House - Semi-Detached'), ('house_detached', 'House - Detached'))), ('Flat', (('maisonette_ground_floor', 'Maisonette - Ground Floor'), ('maisonette_top_floor', 'Maisonette - Top Floor'), ('flat_ground_floor', 'Flat - Ground Floor'), ('flat_upper_floor', 'Flat - Upper Floors'))), ('Bungalow', (('bungalow_semi_detached', 'Bungalow - Semi-Detached'), ('bungalow_detached', 'Bungalow - Detached'))), ('Other', (('commercial', 'Commercial'), ('land', 'Land'), ('other', 'Other')))], max_length=25)),
                ('number_of_bedrooms', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('marketed_from_date', models.DateField()),
                ('offer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord', to='touts.landlord')),
            ],
            options={
                'verbose_name': 'Marketing Information',
                'verbose_name_plural': 'Marketing Information',
                'ordering': ['landlord__landlord_property__postcode', 'landlord__landlord_property__address_line_1', 'landlord__landlord_name'],
            },
        ),
    ]