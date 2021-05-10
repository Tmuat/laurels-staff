# Generated by Django 3.2 on 2021-05-08 11:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created_by", models.CharField(blank=True, max_length=100)),
                ("updated_by", models.CharField(blank=True, max_length=100)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "Regions",
                "ordering": ["name"],
            },
        ),
    ]