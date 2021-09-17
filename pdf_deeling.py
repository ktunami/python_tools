# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 13:25 
# @Author : Kate
# @File : pdf_deeling.py
# @

import os
from PyPDF2 import PdfFileMerger
from setting import *


def merge_pdfs(src_folder, output_name):
    """ 将某文件夹下的pdf合并为一个pdf
    :param src_folder: 文件夹名
    :param output_name: 合并后的文件名
    """
    src_dir = src_path + src_folder
    pdf_lst = [f for f in os.listdir(src_dir) if f.endswith('.pdf')]
    pdf_lst.sort()
    pdf_lst = [os.path.join(src_dir, filename) for filename in pdf_lst]
    out_file = tar_dir + '/' + output_name + '.pdf'
    file_merger = PdfFileMerger()
    print('合并了', len(pdf_lst), '个文件')
    for pdf in pdf_lst:
        file_merger.append(pdf)     # 合并pdf文件
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
        merge_pdfs(c_dir, sub_folder)

