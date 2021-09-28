# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 13:25 
# @Author : Kate
# @File : pdf_dealing.py
# @

import os
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import pdfkit

from setting import *
import os
import asyncio
from pyppeteer import launch
from setting import *
from markdown import markdown


async def save_pdf(url, pdf_path):
    """
    导出pdf
    :param url: 在线网页的url
    :param pdf_path: pdf存放位置
    :return:
    """
    browser = await launch()
    page = await browser.newPage()
    # 加载指定的网页url
    await page.goto(url)
    # 设置网页显示尺寸
    await page.setViewport(view_port)
    '''
    path: 图片存放位置
    width: 纸张宽度，带单位的字符串
    height: 纸张高度，带单位的字符串
    '''
    await page.pdf({'path': pdf_path, 'width': '595px', 'height': '842px'})
    await browser.close()


def get_pdf_from_url(pdf_path, web_url):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_pdf(web_url, pdf_path))


def merge_pdfs(src_folder, output_name, add_bookmark=False):
    """ 将某文件夹下的pdf合并为一个pdf
    :param src_folder: 文件夹名
    :param output_name: 合并后的文件名
    :param add_bookmark: 是否加bookmark
    """
    src_dir = src_path + src_folder
    print(src_dir)
    pdf_lst = [f for f in os.listdir(src_dir) if f.endswith('.pdf')]
    pdf_lst.sort(key=lambda x: float(x.split('_')[0]))
    print(pdf_lst)
    pdf_lst = [os.path.join(src_dir, filename) for filename in pdf_lst]
    out_file = tar_dir + '/' + output_name + '.pdf'
    file_merger = PdfFileMerger()
    print('合并了', len(pdf_lst), '个文件')
    for pdf in pdf_lst:
        chap_name = None
        if add_bookmark:
            chap_name = os.path.split(pdf)[1][:-4]
        file_merger.append(pdf, bookmark=chap_name)
        print('add file: ',pdf)
    file_merger.write(out_file)


def merge_pdfs_sub_folder(src_folder):
    """将某文件夹下所有子文件夹中的pdf分别合并为一个pdf
       合并的文件夹名和子文件夹名相同
       :param src_folder: 文件夹名
    """
    src_dir = src_path + src_folder
    sub_folders = os.listdir(src_dir)
    sub_folders.remove('.DS_Store')
    sub_folders.sort()
    for sub_folder in sub_folders:
        c_dir = src_folder + '/' + sub_folder
        print(c_dir)
        merge_pdfs(c_dir, sub_folder, True)


def md_to_pdf(input_path):
    """
    MarkDown转pdf
    :param input_path: md文档路径
    :return:
    """
    output_path = tar_dir
    res, output_name = os.path.split(input_path)
    output_name = output_name.replace('.md', '.pdf')
    output_path = output_path + os.sep + output_name
    config = "pandoc '{}' -o '{}' --pdf-engine=xelatex -V mainfont='PingFang SC' --template=template.tex"
    config = config + " --resource-path=" + '.:' + res
    print(config)
    cmd = config.format(input_path, output_path)
    os.system(cmd)