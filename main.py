# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/17 09:37
# @Author : Kate
# @File : main.py

from common_files_dealing import FilesDeal as dd
from pdf_dealing import PDF


if __name__ == "__main__":
    # dd.separate_files_to_folders('jjj/刷题python版html', '刷题python版html',  1, 1400, 50, '.')
    # PDF.merge_pdfs_sub_folder('jjj', PDF.get_sort_key('.'))
    # dd.deal_files_cascade('jjj', 'md', PDF.md_to_pdf_callback)
    # dd.deal_files_cascade('jjj', 'html', PDF.html_to_pdf_callback)
    # PDF.merge_pdfs_sub_folder('jjj')
    # dd.print_file_names('jjj')
    # PDF.split_pdf_pages('1.2_极大似然估计.pdf', 2, 5, '1.2_极大似然估计.pdf')
    PDF.get_book_mark_list('a.txt', 2, 'BDA3.pdf', 9)
    print('hello')
