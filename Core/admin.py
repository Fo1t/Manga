from django.contrib import admin
from .models import MangaTitle, MangaChapter, Image, MangaChapterStatus, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']


class CategoryInLine(admin.StackedInline):
    model = MangaTitle.categories.through
    #list_display = ('slug', 'name')


class ImageInLine(admin.StackedInline):
    model = Image


class MangaChapterInLine(admin.StackedInline):
    model = MangaChapter
# @admin.register(MangaTitle)
# class MangaTitleAdmin(admin.ModelAdmin):
#     model = MangaTitle
#     list_display = ('title_name', 'slug', 'image')
#     inlines = [CategoryInLine]

@admin.register(MangaTitle)
class CustomMangaTitleAdmin(admin.ModelAdmin):
    list_display = ('title_name', 'slug', 'image')
    inlines = [CategoryInLine, MangaChapterInLine]


@admin.register(MangaChapter)
class MangaChapterAdmin(admin.ModelAdmin):
    model = MangaChapter
    list_display = ('manga', 'chapter_name', 'URL')
    inlines = [ImageInLine]


@admin.register(MangaChapterStatus)
class MangaChapterStatusAdmin(admin.ModelAdmin):
    model = MangaChapterStatus
    list_display = ('chapter', 'user', 'status')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ('id', 'chapter', 'image_number', 'image')


# @admin.register(UserSettings)
# class ImageAdmin(admin.ModelAdmin):
#     model = UserSettings
#     list_display = ('id', 'user', 'mode')