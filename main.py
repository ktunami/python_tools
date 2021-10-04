# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/17 09:37
# @Author : Kate
# @File : main.py

from common_files_dealing import FilesDeal as dd


if __name__ == "__main__":
    dd.separate_files_to_folders('jjj/刷题python版html', '刷题python版html',  1, 1400, 50, '.')
    # PDF.merge_pdfs_sub_folder('jjj', PDF.get_sort_key('.'))
    # dd.deal_files_cascade('jjj', 'html', dd.del_files_callback)

