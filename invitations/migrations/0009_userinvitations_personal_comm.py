# Generated by Django 3.2.4 on 2021-07-23 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0008_alter_userinvitations_invited'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinvitations',
            name='personal_comm',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=4),
        ),
    ]
