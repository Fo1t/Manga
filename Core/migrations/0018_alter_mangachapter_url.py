# Generated by Django 4.0.5 on 2022-07-21 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0017_mangatitle_dir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangachapter',
            name='URL',
            field=models.URLField(max_length=255, null=True, verbose_name='URL'),
        ),
    ]
