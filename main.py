# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/17 09:37
# @Author : Kate
# @File : main.py

from pdf_dealing import *
import common_files_dealing as F
import pdfkit
from common_files_dealing import *

if __name__ == "__main__":
   # merge_pdfs_sub_folder('jjj')
   deal_sub_files('Python-100-Days-master', 'md', md_to_pdf)
   # md_to_pdf('/Users/kate/Desktop/Python-100-Days-master/Day31-35/31-35.玩转Linux操作系统.md')
