# Generated by Django 3.2.10 on 2022-01-03 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_auto_20220103_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardsinfo',
            name='address2',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='boardsinfo',
            name='agentnotes',
            field=models.CharField(default='', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='boardsinfo',
            name='county',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]