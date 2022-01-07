# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/24 10:02
# @Author : Kate
# @File : web_scraping.py

import os
import re

from bs4 import BeautifulSoup
import random
import time
import socket
import http.client
from common_files_dealing import FilesDeal as dd
from setting import *
import requests
import chardet


def get_html(url):
    """
    获取网页源码
    :param url: 网页url
    :return:
    """
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8, '
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
            # rep = requests.get(url, headers=header, timeout=timeout)
            rep = requests.get(url, timeout=timeout)
            # rep.encoding = rep.apparent_encoding
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


def save_part_html(href, name, err, css_style=''):
    """
    获取网页部分html并存储
    :param href: 网页链接
    :param name: 标题
    :param err: 错误信息
    :param css_style: 样式
    :return:
    """
    href = 'https://www.baidu.com'
    sp = BeautifulSoup(get_html(href), features="html.parser")
    # content = sp.find('div', class_='article_content')
    # content = sp.find('div', class_='markdown_views prism-tomorrow-night-eighties')
    print(sp)
    content = sp.find('article')
    src_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Document</title>
    </head>
    <body>
        <p style='font-size:25px;text-align:center'>{title}</p>
        <br/>
        {content}
    </body>
    <style> {page_style} </style>
    </html>
    '''
    dd.make_dir(SRC_PATH + HTML_FOLDER)
    try:
        with open(SRC_PATH + HTML_FOLDER + os.sep + name + '.html', mode='w+', encoding='utf-8') as f:
            f.write(src_html.format(title=name, content=str(content), page_style=css_style))
    except Exception as ex_results:
        err.append('get_part_html错误：start---->')
        err.append(href)
        err.append(name)
        err.append(ex_results)
        err.append('get_part_html错误：<----end')


def get_hrefs_titles(start, end, content):
    """
    列表中分别获取href和相应标题
    :param start: 从start开始
    :param end: 到end为止
    :param content: html列表（每个元素含一个href和一个title）
    :return:
    """
    lis = content.find_all('a')
    if end == 0:
        lis = lis[start:]
    else:
        lis = lis[start:end]
    links = [li['href'] for li in lis]
    texts = [li.text for li in lis]
    return links, texts


def remove_cur_page_links(links, names):
    """
    将本页链接去除
    :param links: 链接列表
    :param names: 标题列表
    :return: 处理后的链接和标题列表
    """
    pattern = re.compile(r'^#')
    new_href = []
    new_title = []
    for href, title in zip(links, names):
        if not pattern.match(href):
            new_href.append(href)
            new_title.append(title)
    return new_href, new_title


def print_links_titles(links, names):
    """
    打印链接和标题
    :param links: 链接列表
    :param names: 标题列表
    :return:
    """
    l = 0
    for href, title in zip(links, names):
        print(href, '  -', l, '-  ', title)
        l = l + 1


def get_pages_direct(links, names, use_base=False, base_url=None):
    """
    获取并保存页面html，保存名称为names
    :param links: 页面链接
    :param names: 保存名称
    :param use_base:  是否用base_url
    :param base_url: 根目录
    :return:  返回错误信息
    """
    err = []
    for href, title in zip(links, names):
        tit = title.strip()
        if use_base:
            save_part_html(base_url + '/' + href, tit.replace('/', ''), err)
        else:
            save_part_html(href, tit.replace('/', ''), err)
    return err


if __name__ == "__main__":
    the_url = "https://blog.csdn.net/b1055077005/article/details/100152102"
            # "https://pandas.pydata.org/pandas-docs/stable/_images/series_plot_basic.png"
    soup = BeautifulSoup(get_html(the_url), features="html.parser")
    div = soup.find('div', class_='markdown_views prism-tomorrow-night-eighties')
    # div = soup.find('table')
    # hrefs, titles = get_hrefs_titles(0, 0, div)
    # print(get_pages_direct(hrefs, titles, True, the_url))
    err = []
    save_part_html(the_url, 'aaa', err)

