# Generated by Django 4.0.5 on 2022-08-16 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0020_image_image_url_mangachapter_dir_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangachapter',
            name='chapter_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]