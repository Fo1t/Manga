# Generated by Django 4.0.5 on 2022-08-28 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0023_rename_usersattings_usersettings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserSettings',
        ),
    ]
