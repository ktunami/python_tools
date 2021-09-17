# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 12:38 
# @Author : Kate
# @File : del_file.py 
# @

import os
import glob
from setting import *


def del_subfolder_files(src_folder, file_type, remain_num):
    """ 将某路径下的所有子文件夹中的同类型文件的后n个都删除
    :param src_folder: 文件夹名
    :param file_type: 文件类型
    :param remain_num: 保留数目
    """
    src_dir = src_path + src_folder
    dirs = os.listdir(src_dir)
    file_name = '/*.' + file_type
    dirs.remove('.DS_Store')
    for path in dirs:
        c_dir = src_dir + '/' + path
        file_names = glob.glob(c_dir + file_name)
        all_del_files = file_names[remain_num:]
        if len(all_del_files) > 0:
            for it in all_del_files:
                os.remove(it)


def del_folder_files(src_folder, file_type, remain_num):
    """ 删除某文件夹下某类型的文件
    :param src_folder: 文件夹名
    :param file_type: 文件类型
    :param remain_num: 保留个数
    :return:
    """
    src_dir = src_path + src_folder
    file_name = '/*.' + file_type
    file_names = glob.glob(src_dir + file_name)
    files = file_names[remain_num:]
    if len(files) > 0:
        for item in files:
            os.remove(item)
