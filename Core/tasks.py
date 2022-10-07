import logging
import uuid
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from Manga.celery import app
from Core.parse import Parse
import time
from .models import MangaTitle, MangaChapter, MangaChapterStatus, Category, Image
import random
 

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

@app.task
def title_update(manga_list=manga_list, single=False):
    if single:
        print(f'{manga_list} start...')
        parser = Parse(manga_list)
        data = parser.get_data()
        if not data['need_auth']:
            #time.sleep(1)
                #print(f'{manga}')
                #title_update.delay(manga)
            check_category(data['categories'])
            check_title(data)
        print(f'{manga_list} stop...')
    else:
        for manga in manga_list:
            print(f'{manga} start...')
            parser = Parse(manga)
            data = parser.get_data()
            if not data['need_auth']:
            #time.sleep(1)
                #print(f'{manga}')
                #title_update.delay(manga)
                check_category(data['categories'])
                check_title(data)
            print(f'{manga} stop...')
    #print(f'task->title_update->{manga=}')
    # UserModel = get_user_model()
    # try:
    #     user = UserModel.objects.get(pk=user_id)
    #     send_mail(
    #         'Verify your QuickPublisher account',
    #         'Follow this link to verify your account: '
    #             'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
    #         'from@quickpublisher.dev',
    #         [user.email],
    #         fail_silently=False,
    #     )
    # except UserModel.DoesNotExist:
    #     logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    #logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    #time.sleep(10)
    #logging.warning("in tasks")
    #time.sleep(10)
    #parser = Parse(manga)
    #data = parser.get_data()
    #print(f'{data["rus_name"]} start...')
    #if not data['need_auth']:
    #    check_category(data['categories'])
    #    check_title(data)
    #print(f'{data["rus_name"]} stop...')


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
    for chapter in data['chapter_list'][-1:0:-1]:
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


def check_category(categories: list):
    for category in categories:
        if not Category.objects.filter(name=category['name']).exists():
            new_category = Category(name=category['name'])
            new_category.save()