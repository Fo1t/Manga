from django.contrib.auth.models import User
from rest_framework import serializers

from .models import MangaTitle, MangaChapter, Image, MangaChapterStatus


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image_number', 'image')


class MangaChapterStatusSerializers(serializers.ModelSerializer):
    # chapter = MangaChapterSerializers(many=True)
    # user = User(many=True)

    class Meta:
        model = MangaChapterStatus
        fields = ('chapter', 'user', 'status')


class MangaChapterSerializers(serializers.ModelSerializer):
    image = ImageSerializers(many=True)

    # status = MangaChapterStatusSerializers(many=False)

    class Meta:
        model = MangaChapter
        fields = ('id', 'manga', 'URL', 'chapter_number', 'image')


class MangaTitleSerializers(serializers.ModelSerializer):
    #chapter = MangaChapterSerializers(many=True)

    class Meta:
        model = MangaTitle
        fields = ('id', 'title_name', 'slug', 'image', 'image_url', 'mode')
        #fields = ('title_name', 'slug', 'image', 'categories', 'parser_ulr', 'chapter')
