# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 13:25 
# @Author : Kate
# @File : pdf_dealing.py
# @

from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
import pdfkit
import os
import re
import asyncio
from pyppeteer import launch
from itertools import groupby
from setting import *


class PDF(object):

    @staticmethod
    async def _save_pdf(url, pdf_path):
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
        await page.setViewport(VIEW_PORT)
        '''
        path: 图片存放位置
        width: 纸张宽度，带单位的字符串
        height: 纸张高度，带单位的字符串
        '''
        await page.pdf({'path': pdf_path, 'width': PAPER_WIDTH, 'height': PAPER_HEIGHT})
        await browser.close()

    @classmethod
    def get_pdf_from_url(cls, pdf_path, web_url):
        """
        将网页保存为pdf
        :param pdf_path: pdf保存路径
        :param web_url: 网页url
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(cls._save_pdf(web_url, pdf_path))

    @classmethod
    def get_sort_key(cls, delimiter=None):
        if delimiter is not None:
            return lambda x: float(x.split(delimiter)[0])
        else:
            return None

    @classmethod
    def merge_pdfs(cls, src_folder, output_name, sort_key=None, add_bookmark=False):
        """ 将某文件夹下的pdf合并为一个pdf
        :param src_folder: 文件夹名
        :param output_name: 合并后的文件名
        :param add_bookmark: 是否加bookmark
        :param sort_key: pdf排序方式
        """
        src_dir = SRC_PATH + src_folder
        print(src_dir)
        pdf_lst = [f for f in os.listdir(src_dir) if f.endswith('.pdf')]
        pdf_lst.sort(key=sort_key)
        for f in pdf_lst:
            print(f)
        pdf_lst = [os.path.join(src_dir, filename) for filename in pdf_lst]
        out_file = TAR_DIR + '/' + output_name + '_tmp' + '.pdf'
        out_file_final = TAR_DIR + '/' + output_name + '.pdf'
        file_merger = PdfFileMerger()
        print('合并了', len(pdf_lst), '个文件')
        all_sub_marks = []
        for pdf_pt in pdf_lst:
            chap_name = None
            if add_bookmark:
                chap_name = os.path.split(pdf_pt)[1][:-4]
                print(chap_name)
            with open(pdf_pt, 'rb') as f:
                pdf = PdfFileReader(f)
                all_sub_marks.append(pdf.getOutlines())
                print(type(all_sub_marks[0]))
                file_merger.append(pdf, bookmark=chap_name, import_bookmarks=False)
            print('add file: ', pdf_pt)
        file_merger.write(out_file)
        file_merger.close()
        with open(out_file, 'rb') as f:
            pdf = PdfFileReader(f)
            output = PdfFileWriter()
            output.appendPagesFromReader(pdf)
            base_marks = pdf.getOutlines()
            for i in range(len(base_marks)):
                base_mark = base_marks[i]
                base_page = base_mark['/Page']
                parent = output.addBookmark(base_mark['/Title'], base_page)
                for j in all_sub_marks[i]:
                    output.addBookmark(j['/Title'], base_page + j['/Page'], parent=parent)
            with open(out_file_final, 'wb') as f:
                output.write(f)

    @classmethod
    def merge_pdfs_sub_folder(cls, src_folder, sub_sort_key=None, add_bookmark=True):
        """将某文件夹下所有子文件夹中的pdf分别合并为一个pdf
           合并的文件夹名和子文件夹名相同
           :param src_folder: 文件夹名
           :param add_bookmark: 是否添加书签
           :param sub_sort_key: 子文件夹中pdf排序方法
        """
        src_dir = SRC_PATH + src_folder
        sub_folders = os.listdir(src_dir)
        if '.DS_Store' in sub_folders:
            sub_folders.remove('.DS_Store')
        sub_folders.sort()
        for sub_folder in sub_folders:
            c_dir = src_folder + os.sep + sub_folder
            print(c_dir)
            cls.merge_pdfs(c_dir, sub_folder, sub_sort_key, add_bookmark)

    @staticmethod
    def md_to_pdf_callback(input_file_path, output_folder, err):
        """
        Markdown转pdf (多用于批量处理文件)
        :param input_file_path: markdown文件
        :param output_folder: pdf输出的文件夹
        :param err: 错误信息列表
        :return:
        """
        try:
            res, file_name = os.path.split(input_file_path)
            title = file_name.replace('.md', '.pdf')
            config = "pandoc '{}' -o '{}' --pdf-engine=xelatex -V mainfont='PingFang SC' --template=template.tex"
            config = config + " --resource-path=" + '.:' + res
            cmd = config.format(input_file_path, output_folder + os.sep + title)
            os.system(cmd)
        except Exception as ex_results:
            err.append('md_to_pdf错误：start---->')
            err.append(input_file_path)
            err.append(output_folder)
            err.append(ex_results)
            err.append('md_to_pdf错误：<----end')

    @staticmethod
    def html_to_pdf_callback(src_file_path, output_path, err):
        """
        html转pdf (多用于批量处理文件)
        :param src_file_path: html文件
        :param output_path: pdf输出文件夹
        :param err: 错误信息列表
        """
        try:
            file_name = os.path.split(src_file_path)[1]
            title = file_name.replace('.html', '.pdf')
            print(src_file_path)
            print(output_path + os.sep + title)
            pdfkit.from_file(src_file_path, output_path + os.sep + title)
        except Exception as ex_results:
            err.append('md_to_pdf错误：start---->')
            err.append(src_file_path)
            err.append(output_path)
            err.append(ex_results)
            err.append('md_to_pdf错误：<----end')

    @staticmethod
    def split_pdf_pages(file_path, st, end_page, output_name):
        output = PdfFileWriter()
        input_path = SRC_PATH + file_path
        pdf_file = PdfFileReader(open(input_path, "rb"))
        start_page = st - 1
        for i in range(start_page, end_page):
            output.addPage(pdf_file.getPage(i))
        output_stream = open(TAR_DIR + os.sep + output_name, "wb")
        output.write(output_stream)


    @classmethod
    def add_book_marks_cascate(cls, output, bias, idx, book_mark, level, parent, parent_num):
        if idx[level] < len(book_mark[level]):
            if parent is None:
                p = output.addBookmark(book_mark[level][idx[level]][1], book_mark[level][idx[level]][2] + bias, parent=parent)
                if level + 1 < len(idx):
                    cls.add_book_marks_cascate(output, bias, idx, book_mark, level + 1, p, book_mark[level][idx[level]][0])
                idx[level] += 1
                cls.add_book_marks_cascate(output, bias, idx, book_mark, level, parent, parent_num)
            else:
                if book_mark[level][idx[level]][0].startswith(parent_num):
                    p = output.addBookmark(book_mark[level][idx[level]][1], book_mark[level][idx[level]][2] + bias, parent=parent)
                    if level+1 < len(idx):
                        cls.add_book_marks_cascate(output, bias, idx, book_mark, level + 1, p, book_mark[level][idx[level]][0])
                    idx[level] += 1
                    cls.add_book_marks_cascate(output, bias, idx, book_mark, level, parent, parent_num)

    @classmethod
    def get_book_mark_list(cls, book_mark_file, levels, pdf_file, bias):
        book_mark = [[] for i in range(levels)]
        with open(SRC_PATH + book_mark_file, "r") as f:
            for line in f.readlines():
                if line.strip() == '':
                    continue
                raw_list = [''.join(list(g)) for k, g in groupby(line.strip(), key=lambda x: x.isdigit())]
                title = ''.join(raw_list[:-1])
                page = int(raw_list[-1])
                item_number = (re.findall(r'[0-9|.]+', title)[0]).strip()
                if item_number[-1] == '.':
                    item_number = item_number[:-1]
                dot_num = item_number.count('.')
                book_mark[dot_num].append([item_number, title, page])
        with open(SRC_PATH + pdf_file, 'rb') as f:
            pdf = PdfFileReader(f)
            output = PdfFileWriter()
            output.appendPagesFromReader(pdf)
            idx = [0 for i in range(levels)]
            cls.add_book_marks_cascate(output, bias, idx, book_mark, 0, None, None)
            with open(TAR_DIR + os.sep + pdf_file, 'wb') as f:
                output.write(f)


