# Generated by Django 4.0.5 on 2022-07-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0014_remove_category_slug_alter_mangatitle_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название категории'),
        ),
    ]
