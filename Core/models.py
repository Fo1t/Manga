import os
import random
import uuid
from django.db import models
from django.contrib.auth.models import User
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings


# Create your models here.

class Category(models.Model):
    # slug = models.SlugField(max_length=255, verbose_name="Category URL", db_index=True, unique=True)
    name = models.CharField(max_length=255, verbose_name="Название категории", unique=True)

    def __str__(self):
        return "%s" % self.name


class MangaTitle(models.Model):
    def save_override(self, filename):
        media_path = os.path.join(os.path.dirname(settings.MEDIA_ROOT), "media")
        # path1 = os.path.join(os.path.dirname(media_path), "Title")
        # ath2 = os.path.join(os.path.dirname(path1), f'{uuid.uuid1(random.randint(0, 281474976710655))}')
        # path3 = os.path.join(os.path.dirname(path2), f'{uuid.uuid1(random.randint(0, 1000))}')
        # path4 = os.path.join(os.path.dirname(path3), f'{filename}')
        # print(f'{media_path=}\n{path1=}\n{path2=}\n{path3=}\n{path4=}')
        self.dir = str(uuid.uuid1(random.randint(0, 281474976710655)))
        temp_dir = os.path.join(os.path.dirname(settings.MEDIA_ROOT), 'media', f'{self.dir}')
        if not os.path.exists(os.path.join(os.path.dirname(settings.MEDIA_ROOT), f'{self.dir}')):
            #print(f'{temp_dir=}')
            #os.mkdir(f'{temp_dir}')
            pass
        #path1 = os.path.join(os.path.dirname(settings.BASE_DIR), 'media',
        #                     f'Title\{}',
        #                     f'{filename}')
        #print(f'{path1}')
        return os.path.join(os.path.dirname(settings.MEDIA_ROOT), 'media', f'{self.dir}', f'{filename}')  # f'Title\\{uuid.uuid1(random.randint(0, 281474976710655))}\\{uuid.uuid1(random.randint(0, 1000))}\\{filename}'

    title_name = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, verbose_name="URL", db_index=True, unique=True)
    # image_link = models.URLField(max_length=255, verbose_name="Ссылка на картинку")
    image = models.ImageField(upload_to=save_override, null=True)
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    parser_ulr = models.URLField(max_length=255, verbose_name="Ссылка для парсера", null=True)
    dir = models.CharField(max_length=255, null=True)
    image_url = models.URLField(max_length=255, null=True)
    AVAILABILITY_STATUS = [
        ('d', 'Download'),
        ('o', 'Online'),
    ]
    mode = models.CharField(max_length=1, choices=AVAILABILITY_STATUS, default='o', verbose_name="Режим")

    def __str__(self):
        return "%s" % self.title_name

    def get_image_from_url(self, url):
        img_tmp = NamedTemporaryFile(delete=True)
        with urlopen(url) as uo:
            assert uo.status == 200
            img_tmp.write(uo.read())
            img_tmp.flush()
        img = File(img_tmp)
        self.image.save(img_tmp.name, img)
        self.image_url = url


class MangaChapter(models.Model):
    manga = models.ForeignKey(MangaTitle, on_delete=models.CASCADE, related_name='chapter')
    id = models.AutoField(primary_key=True)
    chapter_number = models.FloatField(verbose_name="Номер главы")
    chapter_name = models.CharField(max_length=255, null=True)
    #chapter_number = models.CharField(max_length=255, verbose_name="Номер главы")
    URL = models.URLField(max_length=255, verbose_name="URL", null=True)
    dir = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['chapter_number']

    def __str__(self):
        # return "%s" % self.id
        return f'{self.manga} chapter:{self.chapter_name}'


class MangaChapterStatus(models.Model):
    chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    AVAILABILITY_STATUS = [
        ('r', 'Read'),
        ('u', 'Unread'),
        ('n', 'No information'),
    ]
    status = models.CharField(max_length=1, choices=AVAILABILITY_STATUS, default='n', verbose_name="Статус")
    # status = models.IntegerField(null=False, default=0)


class Image(models.Model):

    def save_override(self, filename):
        return f'Image/{uuid.uuid1(random.randint(0, 281474976710655))}/{uuid.uuid1(random.randint(0, 1000))}{filename}'

    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE, related_name='image')
    # link = models.URLField(max_length=255, verbose_name="URL")
    image_number = models.IntegerField(default=0)
    image = models.ImageField(upload_to=save_override, null=True)
    default_url = 'https://img.freepik.com/free-vector/oops-404-error-with-a-broken-robot-concept-illustration_114360-1932.jpg?w=2000'
    image_url = models.URLField(max_length=255, default=default_url, null=True)

    class Meta:
        ordering = ['image_number']


# class UserSettings(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     AVAILABILITY_MODE = [
#         ('l', 'Light'),
#         ('d', 'Dark'),
#         ('n', 'No information'),
#     ]
#     mode = models.CharField(max_length=1, choices=AVAILABILITY_MODE, default='n', null=False)
# class NewChapter(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     manga_title = models.ForeignKey(MangaTitle, on_delete=models.CASCADE)
#     manga_chapter = models.ForeignKey(MangaChapter, on_delete=models.CASCADE)
