# Generated by Django 4.0.5 on 2022-06-24 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Core', '0006_mangatitle_image_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='MangaChapterStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('chapter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Core.mangachapter')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
