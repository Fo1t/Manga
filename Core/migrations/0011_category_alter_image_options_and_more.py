# Generated by Django 4.0.5 on 2022-07-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0010_alter_mangatitle_url_alter_mangatitle_image_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category URL')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['image_number']},
        ),
        migrations.AlterModelOptions(
            name='mangachapter',
            options={'ordering': ['chapter_number']},
        ),
        migrations.RemoveField(
            model_name='mangatitle',
            name='URL',
        ),
        migrations.RemoveField(
            model_name='mangatitle',
            name='last_read',
        ),
        migrations.AddField(
            model_name='image',
            name='image_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mangatitle',
            name='slug',
            field=models.SlugField(default=1, max_length=255, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mangachapterstatus',
            name='status',
            field=models.CharField(choices=[('r', 'Read'), ('u', 'Unread'), ('n', 'No information')], default='n', max_length=1),
        ),
        migrations.AlterField(
            model_name='mangatitle',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='mangatitle',
            name='categories',
            field=models.ManyToManyField(null=True, to='Core.category'),
        ),
    ]
