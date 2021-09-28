# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/24 10:02
# @Author : Kate
# @File : web_scraping.py
import pdfkit
from bs4 import BeautifulSoup
import requests
import csv
import random
import time
import socket
import http.client
import os
from setting import *
from pdf_dealing import *
import re
from common_files_dealing import *

the_url = "https://numpy123.com"


def get_html(url):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 Safari/537.36 '
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url, headers=header, timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_hrefs_titles(start, end, content):
    lis = content.find_all('a')
    if end == 0:
        lis = lis[start:]
    else:
        lis = lis[start:end]
    links = [li['href'] for li in lis]
    texts = [li.text for li in lis]
    return links, texts


soup = BeautifulSoup(get_html(the_url), features="html.parser")
div = soup.find('div', class_='wy-menu wy-menu-vertical')

hrefs, titles = get_hrefs_titles(0, 0, div)


pattern = re.compile(r'^#')
new_href = []
new_title = []
for href, title in zip(hrefs, titles):
    if not pattern.match(href):
        new_href.append(href)
        new_title.append(title)
hrefs = new_href
titles = new_title

l = 0
for href, title in zip(hrefs, titles):
    print(href, '  -', l, '-  ', title)
    l = l + 1

topics = ['numpy基础篇', 'numpy进阶篇', '深度学习基础教程', 'numpy手册', 'numpy常用API']


def get_path(num):
    if 1 <= num <= 5:
        return True, topics[0]
    elif 6 <= num <= 10:
        return True, topics[1]
    elif 11 <= num <= 22:
        return True, topics[2]
    elif 29 <= num <= 40:
        return True, topics[3]
    elif 41 <= num <= 71:
        return True, topics[4]
    else:
        return False, None


def get_pages_direct():
    folder = src_path + 'jjj' + os.sep
    i = 0
    for href, title in zip(hrefs, titles):
        flag, name = get_path(i)
        if flag:
            sub_url = the_url + href
            sub_path = folder + name + os.sep + str(i) + '_' + title.replace('/', '') + '.pdf'
            print(sub_path, sub_url)
            get_pdf_from_url(sub_path, sub_url)
        i = i + 1



def get_pages(keyword, use_href):
    folder = src_path + 'jjj' + os.sep
    i = 1
    for href, title in zip(hrefs, titles):
        flag = False
        if use_href:
            if keyword.match(href):
                flag = True
        else:
            if keyword.match(title):
                flag = True
        if flag:
            sub_url = the_url + '/' + href
            sub_path = folder + os.sep + str(i) + '_' + title.replace('/', '') + '.pdf'
            print(sub_path, sub_url)
            get_pdf_from_url(sub_path, sub_url)
            i = i + 1


def get_sub_pages():
    for href, title in zip(hrefs, titles):
        url = the_url + href
        sub_soup = BeautifulSoup(get_html(url), features="html.parser")
        ul = sub_soup.find_all('li', class_='toctree-l2')
        sub_link = [the_url + li.a['href'][3:] for li in ul]
        sub_title = [li.a.text for li in ul]
        # make folder
        folder = src_path + 'jjj/' + title.replace('/', '')
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            print(folder + ' already exists')
        for sub_link, sub_title in zip(sub_link, sub_title):
            sub_path = folder + '/' + sub_title.replace('/', '') + '.pdf'
            print(sub_path)
            get_pdf_from_url(sub_path, sub_link)


get_pages_direct()