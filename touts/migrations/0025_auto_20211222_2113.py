# Generated by Django 3.2.10 on 2021-12-22 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touts', '0024_rename_offer_marketinginfo_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toutletter',
            name='requested_no_contact',
        ),
        migrations.RemoveField(
            model_name='toutletter',
            name='success',
        ),
        migrations.AddField(
            model_name='toutletter',
            name='do_not_send_reason',
            field=models.CharField(choices=[('laurels_success', 'Laurels Success'), ('off_the_market', 'Off The Market'), ('no_contact', 'Requested No Contact')], max_length=50, null=True),
        ),
    ]
