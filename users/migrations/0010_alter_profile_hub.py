# Generated by Django 3.2 on 2021-05-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionandhub', '0011_alter_hubtargetsyear_hub'),
        ('users', '0009_auto_20210520_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hub',
            field=models.ManyToManyField(related_name='employee', to='regionandhub.Hub'),
        ),
    ]
