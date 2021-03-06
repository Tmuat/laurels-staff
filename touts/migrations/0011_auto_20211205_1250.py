# Generated by Django 3.2.5 on 2021-12-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0010_toutproperty_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='toutletter',
            name='do_not_send',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_five',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_four',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_one',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_six',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_three',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='letter_two',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='requested_no_contact',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='toutletter',
            name='success',
            field=models.BooleanField(default=False),
        ),
    ]
