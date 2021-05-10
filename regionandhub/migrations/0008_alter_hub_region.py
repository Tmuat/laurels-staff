# Generated by Django 3.2 on 2021-05-10 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("regionandhub", "0007_alter_hubtargets_hub_targets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hub",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="region",
                to="regionandhub.region",
            ),
        ),
    ]