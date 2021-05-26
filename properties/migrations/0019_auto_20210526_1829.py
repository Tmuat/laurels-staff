# Generated by Django 3.2 on 2021-05-26 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0018_auto_20210526_1824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offererdetails',
            options={'ordering': ['propertyprocess__property__postcode', 'propertyprocess__property__address_line_1', 'full_name'], 'verbose_name': 'Offerer History', 'verbose_name_plural': 'Offerer History'},
        ),
        migrations.AlterField(
            model_name='offerermortgage',
            name='offerer_details',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='offerer_mortgage_details', to='properties.offererdetails'),
        ),
    ]
