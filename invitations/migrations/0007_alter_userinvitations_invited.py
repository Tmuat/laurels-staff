# Generated by Django 3.2 on 2021-05-17 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invitations", "0006_userinvitations_invite_sent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinvitations",
            name="invited",
            field=models.DateTimeField(),
        ),
    ]
