import os.path
import random
import re
import time

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect
import uuid
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.views.generic.detail import SingleObjectMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AddMangaTitleForm, AddMangaChapterForm
from .models import MangaTitle, MangaChapter, MangaChapterStatus, Category, Image
from .serializers import MangaTitleSerializers
from .parse import Parse
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File  # you need this somewhere
import urllib
from django.conf import settings
import shutil
from tqdm import tqdm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from itertools import groupby

from django.db.models import signals
from Core.tasks import title_update

from sys import platform
from pathlib import Path


class MainApiView(APIView):
    def get(self, request):
        manga = MangaTitle.objects.all().order_by('title_name')
        serializer = MangaTitleSerializers(manga, many=True)
        return Response({"data": serializer.data}, status=200)


def show_title(request, title_slug):
    title = get_object_or_404(MangaTitle, slug=title_slug)
    if not title:
        raise Http404("Title not found")
    context = {'title': title}
    context['chapters'] = MangaChapter.objects.filter(manga=title)
    context['def_chapter'] = context['chapters'][0].id
    return render(request, 'detail.html', context)


@xframe_options_exempt
def chapter_frame(request, chapter_id):
    chapter = get_object_or_404(MangaChapter, id=chapter_id)
    pattern = 'http[s]?:\/(?:\/[^\/]+){1,}(?:\/[А-Яа-яёЁ\w ]+\.[a-z]{3,5}(?![\/]|[\wА-Яа-яёЁ]))'
    if not chapter:
        raise HttpResponse("This page is safe to load in a frame on any site.")
    context = {'chapter': chapter}
    for image in Image.objects.filter(chapter=chapter):
        if image.chapter.manga.mode == 'o':
            if image.image_url != re.search(pattern=pattern, string=image.image_url)[0]:
                image.image_url = re.search(pattern=pattern, string=image.image_url)[0]
                image.save()
    context['images'] = Image.objects.filter(chapter=chapter)
    context['mode'] = chapter.manga.mode
    return render(request, 'frame.html', context)





def extraUpdate(request):
    chapters = MangaChapter.objects.all()
    for chapter in tqdm(chapters):
        if not MangaTitle.objects.filter(id=chapter.manga_id).exists():
            images = Image.objects.filter(chapter_id=chapter.id)
            images.delete()
            chapter.delete()
    #titles.delete()
    # pattern = 'http[s]?:\/(?:\/[^\/]+){1,}(?:\/[А-Яа-яёЁ\w ]+\.[a-z]{3,5}(?![\/]|[\wА-Яа-яёЁ]))'
    # for title in MangaTitle.objects.all()[:100]:
    #     print(f'{title} start')
    #     if title.mode == 'o':
    #         for chapter in tqdm(MangaChapter.objects.filter(manga=title)):
    #             image_list = []
    #             image_query = Image.objects.filter(chapter=chapter)
    #             for image in image_query:
    #                 image_list.append([image.image_url])
    #                 if image.image_url != re.search(pattern=pattern, string=image.image_url)[0]:
    #                     image.image_url = re.search(pattern=pattern, string=image.image_url)[0]
    #                     image.save()
    #             Image.objects.filter(chapter=chapter).delete()
    #             new_image_list = [el for el, _ in groupby(image_list)]
    #             #print(f'{image_list=}\n{new_image_list=}')
    #             image_index = 0
    #             if len(new_image_list) < len(image_query):
    #                 for image in new_image_list:
    #                     new_image = Image(chapter=chapter, image_number=image_index, image_url=image)
    #                     new_image.save()
    #                     image_index += 1
    #                 image_query.delete()
    #     print(f'{title} stop')
    return redirect('/')

class MainPage(ListView):
    model = MangaTitle
    paginate_by = 24
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #re = self.request
        #print(f'{self.request.META=}')
        #print(f'MainPage -> get_context_data -> {self.request.user_settings=}')
        context['now'] = timezone.now()
        print(f'{platform=}')
        print(Path(__file__).resolve().parent.parent)


        return context


class MangaTitleDetailView(DetailView):
    model = MangaTitle
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        chapters_read, chapters_nr = {}, {}
        if self.request.user.is_authenticated:
            for item in MangaChapter.objects.filter(manga=context['object']):
                if MangaChapterStatus.objects.filter(user=self.request.user, chapter=item).exists():
                    chapters_read[item] = MangaChapterStatus.objects.get(user=self.request.user, chapter=item).status
                else:
                    chapters_nr[item] = 0
        else:
            chapters_nr = MangaChapter.objects.filter(manga=context['object'])

        context['chapters_read'] = chapters_read
        context['chapters_nr'] = chapters_nr
        return context


def GoToRead(request, pk):
    chapter = MangaChapter.objects.get(id=pk)
    if request.user.is_authenticated:
        user = request.user
        new_chapter_status = MangaChapterStatus(chapter=chapter, user=user, status=1)
        new_chapter_status.save()
    return redirect('/')


def Update(request):
    manga_list = [
        #'Став жертвой, я убил Злого Бога!',
        # 'Боевой Мастер',
        # 'Божественный Император Лин',
        # 'Вечное Почтение',
        # 'Вечный первый бог',
        # 'Владыка Духовного Меча',
        # 'Возвращение Культиватора в Университет',
        # 'Возрождение Городского Божества',
        # 'Воинственный бог Асура',
        # 'Восставший против неба',
        # 'Выживание с нуля',
        # 'Выше Всех Богов',
        # 'Городской бог',
        # 'Групповая Беседа Культиваторов',
        # 'Дракон внутри меня',
        # 'Жизнь императора войны после ухода в отставку',
        # 'Звёздный император',
        # 'Игрок',
        # 'Король Апокалипсиса',
        # 'Культиватор из Будущего',
        # 'Легендарный лунный скульптор',
        # 'Лучший в мире мастер боевых искусств',
        # 'Меч против неба',
        # 'Меч разящего грома',
        # 'Мои ученики - супер боги',
        # 'Мой папа слишком сильный',
        # 'На самом деле, я большой человек на пути культивации',
        # 'Наномашины',
        # 'Невероятное обучение',
        # 'Она представилась как ученица мудреца',
        # 'Перерождение бессмертного горожанина-культиватора',
        # 'Перерождение Бессмертного Императора',
        # 'Пик Боевых Искусств',
        # 'Пойманный в ловушку на миллионы лет: Мои ученики распространились по всему миру',
        # 'Последний человек',
        # 'Почтенный бессмертный Ло Вуцзи',
        # 'Пощади Меня, Великий Господин',
        # 'Прокачка в альтернативном мире',
        # 'Расхититель гробниц',
        # 'Регрессия мага 8-го класса',
        # 'С сегодняшнего дня я лорд города',
        # 'Сильнейший Отброс',
        # 'Сказания о Бессмертных и го',
        # 'Сказания о Демонах и Богах',
        'Становление богом',
        'Техника Бога звёздных боевых искусств',
        'Туториал продвинутого игрока в башне',
        'У меня есть особняк в постапокалиптическом мире',
        'Эволюция монстров-питомцев',
        'Элисед',
        'Юань лун',
        'Я великий Бессмертный',
        'Я злой бог',
        'Я обречен на величие!',
        'Я переживал один и тот же день в течение тысячи лет',
        'Я, сильнейший король демонов, стал ребенком?!',
        'Моя девушка - зомби',
        'Бессмертный мечник в обратном мире',
        'Возрождение великого бога',
        'Я бессмертный',
        'Одинокий странник',
        'Почтенный бессмертный отец',
        'Бессмертный отец',
    ]
    #for manga in manga_list:
    #    print(f'{manga} start...')
    #    parser = Parse(manga)
    #    data = parser.get_data()
    #    if not data['need_auth']:
        #time.sleep(1)
    #        print(f'{manga}')
    title_update.delay()
            #check_category(data['categories'])
    #        check_title(data)
    #    print(f'{manga} stop...')
    return redirect('/')

def update_title(request, title_slug):
    title = get_object_or_404(MangaTitle, slug=title_slug)
    if not title:
        raise Http404("Title not found")
    chapters = MangaChapter.objects.filter(manga=title).all()
    chapters.delete()
    title_update.delay(title.title_name, True)
    return redirect(f'/')
    

def check_title(data: dict):
    #img_url = f'https://api.remanga.org/media/titles/my-three-thousand-years-to-the-sky/2b5f474f165593bda0f20f2ea5e26106.jpg'
    pattern = 'http[s]?:\/(?:\/[^\/]+){1,}(?:\/[А-Яа-яёЁ\w ]+\.[a-z]{3,5}(?![\/]|[\wА-Яа-яёЁ]))'
    if not MangaTitle.objects.filter(title_name=data['rus_name']).exists():
        img_url = f'https://api.remanga.org/{data["img"]}'
        new_title = MangaTitle()
        new_title.title_name = data['rus_name']
        new_title.slug = data['dir']
        dst_path = f'{new_title.save_override(img_url.split("/")[-1])}'
        title_dir = ''
        for x in dst_path.split('\\')[:-1]:
            title_dir += "".join(f'{str(x)}\\')
        new_title.dir = title_dir
        #download_file(img_url, img_url.split("/")[-1], dst_path)
        new_title.image_url = img_url
        #download_file(img_url, dst_path)
        new_title.image = f'media/{img_url.split("/")[-1]}'
        new_title.save()
        for tag in data['categories']:
            name = tag['name']
            category = Category.objects.get(name=name)
            new_title.categories.add(category)
            pass
        new_title.save()
    chapter_index = 0
    for chapter in tqdm(data['chapter_list'][-1:0:-1]):
        if not chapter[2]:
            if not MangaChapter.objects.filter(manga=MangaTitle.objects.get(title_name=data['rus_name']),
                                            chapter_number=chapter[3]).exists():
                manga_title = MangaTitle.objects.get(title_name=data['rus_name'])
                new_chapter = MangaChapter(manga=manga_title, chapter_number=chapter_index, chapter_name=chapter[1])
                chapter_index += 1
                new_chapter.save()
                image_index = 0
                dir_name = str(uuid.uuid1(random.randint(0, 281474976710655)))
                #last_img = Image()
                for image in chapter[-1]:
                    if image is list():
                        image_index += 1
                        for image_part in image:
                            #try:
                                #new_image_ulr = re.search(pattern=pattern, string=str(image[-1]))[0]
                                #print(new_image_ulr)
                                #if last_img.image_url != new_image_ulr:
                                    #download_file(image_part[-1], image_part[-1].split('/')[-1], dir_name)
                            new_image = Image()
                            new_image.chapter = new_chapter
                            new_image.image_url = image_part[-1]
                            #last_img_url = new_image.image_url
                                    #new_image.image = f'media/{image_part[-1].split("/")[-1]}'
                            new_image.image_number = image_part[0]
                            #image_index += 1
                            new_image.save()
                    else:
                        new_image = Image()
                        new_image.chapter = new_chapter
                        new_image.image_url = image[-1]
                        new_image.image_number = image_index
                            #image_index += 1
                        new_image.save()
                        image_index += 1
                        #last_img = new_image
                        #except TypeError:
                        #    pass



def download_file(url, file_path):
    res = requests.get(url, stream=True)
    dir_path = ''
    for x in file_path.split('\\')[:-1]:
        dir_path += "".join(f'{str(x)}\\')
    if not os.path.exists(dir_path):
        os.mkdir(f'{dir_path}')
    if res.status_code == 200:
        with open(f'{file_path}', 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
       print('Image Couldn\'t be retrieved')

def tempfunc():
    img_url = "https://api.remanga.org/media/titles/my-three-thousand-years-to-the-sky/2b5f474f165593bda0f20f2ea5e26106.jpg "
    file_name = img_url.split('/')[-1]
    res = requests.get(img_url, stream=True)
    if res.status_code == 200:
       with open(f'../media/{file_name}', 'wb') as f:
           shutil.copyfileobj(res.raw, f)
    else:
       print('Image Couldn\'t be retrieved')

def check_category(categories: list):
    for category in categories:
        if not Category.objects.filter(name=category['name']).exists():
            new_category = Category(name=category['name'])
            new_category.save()


class AddMangaTitle(LoginRequiredMixin, FormView):
    model = MangaTitle
    form_class = AddMangaTitleForm
    template_name = 'AddManga.html'
    fields = [
        'title_name',
        #'URL',
        #'last_read',
        #'image_link',
    ]

    def post(self, request, *args, **kwargs):
        #MangaTitle(title_name=request.POST['title_name'],
        #           URL=request.POST['URL'],
        #           last_read=request.POST['last_read'],
        #           image_link=request.POST['image_link'],
        #           ).save()
        title_update.delay(request.POST['title_name'], True)
        return redirect('/')

    # def get(self, request):
    #     if not request.user.is_staff:
    #         return HttpResponse("Here's the text of the web page.")
    #     return HttpResponse("Here's the text of the web page.")


class AddMangaChapter(LoginRequiredMixin, FormView):
    model = MangaChapter
    form_class = AddMangaChapterForm
    template_name = 'AddManga.html'
    fields = [
        'chapter_number',
        'URL',
    ]

    def post(self, request, *args, **kwargs):
        MangaChapter(manga=MangaTitle.objects.get(id=kwargs['pk']),
                     chapter_number=request.POST['chapter_number'],
                     URL=request.POST['URL'],
                     ).save()
        # manga = MangaTitle.objects.get(id=1)
        # new_chapter = MangaChapter(manga=manga,
        #            URL=request.POST['URL'],
        #            last_read=request.POST['chapter_number'],
        #            ).save()

        return redirect('/')
