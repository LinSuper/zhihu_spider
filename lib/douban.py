# -*- encoding:utf-8 -*-
##############################
__author__ = "LinSuper"
__date__ = "2015/3/22"
###############################

import requests
from bs4 import BeautifulSoup
import urllib
import re

# loginUrl = 'http://accounts.douban.com/login'
# formData={
#     "redir":"http://movie.douban.com/mine?status=collect",
#     "form_email":'8674925@163.com',
#     "form_password":'abc.-8674925',
#     "login":u'登录'
# }
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1)\
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
requests = requests.Session()
proxies = {
    'http': '222.174.71.46:9797',
    'https': '222.174.71.46:9797'
}
# requests.proxies = proxies
# r = requests.post(loginUrl,data=formData,headers=headers)
# for num in range(50):
#     url = 'https://www.douban.com/group/510760/discussion?start=%s' %(num*25)
#     print url
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.content)
#     tb = soup.find('table',{'class':'olt'})
#     tr=tb.findAll('tr',{'class':''})
#     for i in tr:
#         rap = i.findAll('td', {'class':''})[0]
#         find_link = i.findAll('a')
#         print rap
#         # print find_link[0].attrs['href']
#         # print find_link[0].attrs['title']
#         # print find_link[1].attrs['href']
#         # print find_link[1].text
class Discussion:
    url = None
    soup = None
    def __init__(self, url, title=None):
        self.url = url
        if title:
            self.title = title

    def parser(self):
        r =  requests.get(self.url + '/discussion', headers=headers)
        self.soup = BeautifulSoup(r.content)

    def get_title(self):
        if hasattr(self, 'title'):
            return self.title
        else:
            soup = self.soup
            self.title = soup.find('title').text
            return self.title

    def get_paginator_num(self):
        if self.soup is None:
            self.parser()
        soup = self.soup
        find_paginator = soup.find('div', {'class': 'paginator'})
        find_span = find_paginator.find('span', {'class': 'thispage'})
        page_num = int(find_span.attrs['data-total-page'])
        self.page_num = page_num
        return page_num

    def get_all_topics(self, start_page_num=0):
        if not hasattr(self, 'page_num'):
            self.get_paginator_num()
        for i in xrange(self.page_num):
            if i < start_page_num:
                continue
            if i == 0:
                soup = self.soup

            else:
                r =  requests.get(self.url+ '/discussion?start=%s'%(i * 25), headers=headers)
                print r.url
                soup = BeautifulSoup(r.content)
            tb = soup.find('table',{'class':'olt'})
            tr=tb.findAll('tr',{'class':''})
            for j in tr:
                rap = j.findAll('td', {'class':''})[1].text
                find_link = j.findAll('a')
                if rap:
                    rap = int(rap)
                else:
                    rap = 0
                topic_url = find_link[0].attrs['href']
                topic_title = find_link[0].attrs['title']
                user_url = find_link[1].attrs['href']
                user_name = find_link[1].text
                author = User(user_url, user_name)
                yield Topic(topic_url, topic_title, rap, author)

    def get_top_i_page_topic(self, n):
        j = 0
        topics = self.get_all_topics()
        for topic in topics:
            j += 1
            if j > n * 25:
                break
            yield topic



class Topic:
    topic_url = None
    topic_title = None
    soup = None

    def __init__(self, topic_url, topic_title=None, rap=None, author=None):
        self.topic_url = topic_url
        if topic_title != None:
            self.title = topic_title
        if author != None:
            self.author = author
        self.auth = None
        if rap != None:
            self.rap = rap


    def parser(self):
        r = requests.get(self.topic_url, headers=headers)
        if r.url == self.topic_url:
            self.auth = True
        else:
            self.auth = False
        soup = BeautifulSoup(r.content)
        self.soup = soup


    def get_title(self):
        if self.soup is None:
            self.parser()
        soup = self.soup
        self.title = soup.find('title').text
        return self.title

    def get_author(self):
        if self.soup is None:
            self.parser()
        soup = self.soup
        find_face = soup.find('div', class_='user-face')
        user_url = find_face.find('a').attrs['href']
        user_img_small = find_face.find('img').attrs['src']
        find_topic_doc = soup.find('div', class_='topic-doc')
        user_name = find_topic_doc.find('a').text
        create_time = find_topic_doc.find('span', class_='color-green').text
        self.create_time = create_time
        return User(user_url, user_name, user_img_small)

    def get_image(self):
        if self.soup is None:
            self.parser()
        if not self.auth:
            return []
        soup = self.soup
        img_list = []
        find_content = soup.find('div', class_='topic-content').find('div', class_='topic-content')
        for i in find_content.findAll('img'):
            img_list.append(
                i.attrs['src']
            )
        return img_list



class User:
    user_name = None
    soup = None
    user_url = None

    def __init__(self, user_url, user_name=None, user_img_small=None):
        self.user_url = user_url
        if user_name!= None:
            self.user_name = user_name
        if user_img_small != None:
            self.user_img_small = user_img_small

    def parser(self):
        r = requests.get(self.user_url, headers=headers)
        if r.url == self.user_url:
            self.auth = True
        else:
            self.auth = False
        soup = BeautifulSoup(r.content)
        self.soup = soup

    def get_img_small(self):
        if hasattr(self, 'user_img_small'):
            return self.user_img_small
        if self.soup is None:
            self.parser()
        soup = self.soup
        user_img_small = soup.find('div', class_='pic').find('img').attrs['src']
        self.user_img_samll = user_img_small
        return user_img_small

    def get_img_large(self):
        if self.soup is None:
            self.parser()
        soup = self.soup
        user_img_large = soup.find('div', class_='basic-info').find('img').attrs['src']
        self.user_img_large = user_img_large
        return user_img_large
