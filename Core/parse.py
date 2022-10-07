import math
import random
import time

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
from requests.auth import HTTPBasicAuth

class Parse:
    __sleep = 0.5
    __sleep_random_min = 0
    __sleep_random_max = 1

    def __init__(self, title_name):
        #print(f'Init start')
        self.auth = HTTPBasicAuth('wilase4615', 'wilase4615@mxcdd.com##')
        self.need_auth = True
        self.__api_url = 'https://api.remanga.org/api/'
        self.__media_url = 'https://api.remanga.org/media/'
        api_search_url = self.__api_url + 'search/?query=' + title_name + '&count=1'
        data = requests.get(api_search_url).json()
        self.id = data['content'][0]['id']
        self.en_name = data['content'][0]['en_name']
        self.rus_name = data['content'][0]['rus_name']
        self.dir = data['content'][0]['dir']
        self.bookmark_type = data['content'][0]['bookmark_type']
        self.img = data['content'][0]['img']['high']
        self.issue_year = data['content'][0]['issue_year']
        self.avg_rating = data['content'][0]['avg_rating']
        self.type = data['content'][0]['type']
        #print(f'\n__get_more_informations start\n')
        self.__get_more_informations()
        if not self.need_auth:
        #print(f'\n__get_more_informations stop\n__get_chapters start\n')
            self.__get_chapters()
            #print(f'\n__get_chapters stop\n__get_images_url start\n')
            self.__get_images_url()
        #print(f'\n__get_images_url start\nInit stop\n')

    def __get_more_informations(self):
        url = self.__api_url + 'titles/' + self.dir
        data = requests.get(url, auth=self.auth).json()
        time.sleep(self.__sleep+random.randint(self.__sleep_random_min, self.__sleep_random_max))
        if data['msg'] != 'Для просмотра нужно авторизироваться':
            self.need_auth = False
            self.categories = data['content']['genres'] + data['content']['categories']
            self.count_chapters = data['content']['count_chapters']
            #bar = IncrementalBar('Countdown', max=len(data['content']['branches']))
            for item in tqdm(data['content']['branches']):
                if item['count_chapters'] == self.count_chapters:
                    self.active_branch = item['id']
            #bar.next()
        #bar.finish()

    def get_data(self):
        data = {
            'need_auth': self.need_auth,
            #'chapter_list': self.chapter_list,
        }
        if not self.need_auth:
            data['chapter_list'] = self.chapter_list
            data['count_chapters'] = self.count_chapters
            data['__api_url'] = self.__api_url
            data['id'] = self.id
            data['en_name'] = self.en_name
            data['rus_name'] = self.rus_name
            data['dir'] = self.dir
            data['bookmark_type'] = self.bookmark_type
            data['img'] = self.img
            data['issue_year'] = self.issue_year
            data['avg_rating'] = self.avg_rating
            data['type'] = self.type
            data['categories'] = self.categories
            data['active_branch'] = self.active_branch
        return data

    def __get_chapters(self):
        url = f'{self.__api_url}titles/chapters/?branch_id={self.active_branch}'
        chapter_list = []
        #bar = IncrementalBar('Countdown', max=math.ceil(self.count_chapters / 60 + 1))
        for index in tqdm(range(1, math.ceil(self.count_chapters / 60 + 1))):
            temp_url = url + f'&count=60&page={index}'
            data = requests.get(temp_url).json()
            time.sleep(self.__sleep+random.randint(self.__sleep_random_min, self.__sleep_random_max))
            for item in data['content']:
                chapter_list.append([item['id'], item['chapter'], item['is_paid'], item['index']])
            #bar.next()
        #bar.finish()
        self.chapter_list = chapter_list

    def __get_images_url(self):
        # bar = IncrementalBar('Countdown', max=len(self.chapter_list))
        for item in tqdm(self.chapter_list):
            if not item[2]:
                time.sleep(self.__sleep + random.randint(self.__sleep_random_min, self.__sleep_random_max))
                temp_url = f'{self.__api_url}titles/chapters/{item[0]}/'
                r = requests.get(temp_url)
                try:
                    data = r.json()
                except requests.exceptions.JSONDecodeError:
                    pass
                except KeyError:
                    pass
                except ...:
                    pass
                images = []
                # temp = data['content']['pages']
                # print(f'{temp=}')
                for image in data['content']['pages']:
                    #print(f'\n{image=}\n')
                    if isinstance(image, dict):
                        images.append([image['page'], image['link']])
                    else:
                        image_list = []
                        for img in image:
                            image_list.append([img['page'], img['link']])
                        images.append(image_list)
                        pass
                        #images.append([image[0]['page'], image[0]['link']])
                item.append(images)
        pass
