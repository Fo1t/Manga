# Generated by Django 4.0.5 on 2022-06-20 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangatitle',
            name='URL',
            field=models.URLField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
