# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/3 12:38 
# @Author : Kate
# @File : common_files_dealing.py
# @

import os
import shutil

from setting import *
import re


class FilesDeal(object):

    @staticmethod
    def _get_num_pair(start_num, end_num, span):
        """
        获取起止数值对的列表
        :param start_num: 开始数值
        :param end_num: 结束数值
        :param span: 跨度
        :return: 返回起止数值对的列表
        """
        result = []
        cur_start = start_num
        while cur_start < end_num:
            if (cur_start + span - 1) < end_num:
                result.append((cur_start, cur_start + span - 1))
            else:
                result.append((cur_start, end_num))
            cur_start = cur_start + span
        return result

    @classmethod
    def _get_name_list(cls, base_str, start_num, end_num, span):
        """
        根据数值对列表给出子文件夹名列表
        :param base_str: 子文件夹的公共名字
        :param start_num: 开始数值
        :param end_num: 结束数值
        :param span: 跨度
        :return: 子文件夹名列表
        """
        range_nums = cls._get_num_pair(start_num, end_num, span)
        return [str(n) + '_' + base_str + str(ran_pair[0]) + '-' + str(ran_pair[1])
                for ran_pair, n in zip(range_nums, range(1, len(range_nums) + 1))]

    @classmethod
    def _get_sub_folder(cls, file_name, sep, start_num, span, sub_folder_names):
        """
        获得目标子文件夹名（分文件用）
        :param file_name: 文件名
        :param sep: 分割符
        :param start_num: 开始数值
        :param span: 跨度
        :param sub_folder_names: 子文件夹名列表
        :return: 子文件夹名
        """
        num_str = file_name.split(sep)[0]
        try:
            num = int(num_str)
            idx = (num - (start_num - 1)) // span
            if (num - (start_num - 1)) % span == 0:
                idx = idx - 1
            return sub_folder_names[idx]
        except ValueError as e:
            print(e)
            print('wrong num_str: ', num_str)
        except IndexError as e:
            print(e)
            print('wrong num: ', num)

    @classmethod
    def separate_files_to_folders(cls, src_folder, base_str, start_num, end_num, span, sep):
        sub_folders = cls._get_name_list(base_str, start_num, end_num, span)
        cls.make_src_folders(TAR_COPY_FOLDER, sub_folders)
        src_dir = SRC_PATH + src_folder
        file_names = os.listdir(src_dir)
        for file in file_names:
            tar_sub_folder = cls._get_sub_folder(file, sep, start_num, span, sub_folders)
            try:
                source_file = src_dir + os.sep + file
                target_file = SRC_PATH + TAR_COPY_FOLDER + os.sep + tar_sub_folder + os.sep + file
                shutil.move(source_file, target_file)
            except Exception as e:
                print(e)
                print('source_file', source_file)
                print('target_file', target_file)

    @staticmethod
    def del_files_callback(file_path, err):
        """
        删除某文件
        :param file_path: 文件路径
        :param err: 错误信息
        :return:
        """
        try:
            os.remove(file_path)
            print('removed: ', file_path)
        except Exception as e:
            err.append(file_path)
            err.append(e)
            print(e)

    @staticmethod
    def make_dir(path):
        """
        创建文件夹
        :param path: 文件夹路径
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)
            print('create ' + path)
        else:
            print(path + ' already exists')

    @classmethod
    def make_src_folders(cls, folder, sub_folder_list):
        path = SRC_PATH + folder
        cls.make_dir(path)
        for f in sub_folder_list:
            p = path + os.sep + f
            cls.make_dir(p)

    @staticmethod
    def check_file_type(file_name, file_type):
        """
        查看文件是否为某类型的文件
        :param file_name: 文件名
        :param file_type: 文件类型
        :return:
        """
        pattern = re.compile(r".*\.%s$" % file_type)
        return re.match(pattern, file_name) is not None

    @classmethod
    def _deal_all_files(cls, folder, file_type, err, callback, remain_num=0):
        """
        递归的对folder下类型为file_type的文件用callback进行批量处理，错误信息返回给err
        :param folder: 待处理文件夹
        :param file_type: 文件类型
        :param err: 错误信息列表
        :param callback: 处理函数
        :param remain_num: 保留未处理数目
        :return:
        """
        dirs = os.listdir(SRC_PATH + folder)
        count = 0
        for p in dirs:
            c_dir = SRC_PATH + folder + os.sep + p
            if os.path.isdir(c_dir):
                if callback != cls.del_files_callback:
                    tar_path = TAR_DIR + os.sep + folder + os.sep + p
                    cls.make_dir(tar_path)
                cls._deal_all_files(folder + os.sep + p, file_type, err, callback, remain_num)
            elif cls.check_file_type(p, file_type):
                count = count + 1
                if count > remain_num:
                    if callback != cls.del_files_callback:
                        callback(c_dir, TAR_DIR + os.sep + folder, err)
                    else:
                        callback(c_dir, err)

    @classmethod
    def deal_files_cascade(cls, src_folder, file_type, callback, remain_num=0):
        """
        调用deal_all_files，递归的对src_folder中file_type类型文件进行批量处理
        :param src_folder: 待处理文件夹
        :param file_type: 文件类型
        :param callback: 处理函数
        :param remain_num: 保留未处理数目
        :return 返回错误信息
        """
        if callback != cls.del_files_callback:
            cls.make_dir(TAR_DIR + os.sep + src_folder)
        err = []
        cls._deal_all_files(src_folder, file_type, err, callback, remain_num)
        return err
