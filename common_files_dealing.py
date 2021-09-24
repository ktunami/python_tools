# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 12:38 
# @Author : Kate
# @File : common_files_dealing.py
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


def mkdir(folders):
    """ 创建文件夹
    :param folders: 文件夹名称列表
    """
    for folder in folders:
        path = src_path + folder
        if not os.path.exists(path):
            os.makedirs(path)
            print('create ' + path)
        else:
            print(path + ' already exists')


def change_filename_pdf(folder):
    path = src_path + folder
    files = os.listdir(path)
    n = 0
    for file in files:
        oldname = path + os.sep + file  # os.sep添加系统分隔符
        newname = path + os.sep + file + '.pdf'
        os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
        print(oldname, '======>', newname)
