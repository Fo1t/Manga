# Generated by Django 4.0.5 on 2022-08-16 23:18

import Core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0019_alter_mangachapter_chapter_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(default='https://img.freepik.com/free-vector/oops-404-error-with-a-broken-robot-concept-illustration_114360-1932.jpg?w=2000', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mangachapter',
            name='dir',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mangatitle',
            name='image_url',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mangatitle',
            name='mode',
            field=models.CharField(choices=[('d', 'Download'), ('o', 'Online')], default='o', max_length=1, verbose_name='Режим'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to=Core.models.Image.save_override),
        ),
        migrations.AlterField(
            model_name='mangatitle',
            name='image',
            field=models.ImageField(null=True, upload_to=Core.models.MangaTitle.save_override),
        ),
    ]
