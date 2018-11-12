#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import fitz
import re
import shutil


# 首先得先对PDF进行目录的提取，用来保存需要查找的图表关键字
# 参数需要放入文件名
def catalog_extract(file_name):
    doc = fitz.open(file_name)
    page_count = doc.pageCount
    result = []
    if page_count > 15:
        search_pages = 15
    else:
        search_pages = page_count
    keyword = '.......'
    # keyword1 = r'((?:[图表]+\s*[表]*){1,}\s*\d+.*?)((?:\.{2,}\s*){1,})(\s*\d+)'
    keyword1 = r'((?:[图表]+\s*[表]*){1,}\s*\d+.*?)(\.{2,}\s*)(\s*\d+)'
    num = 0
    flag = 0
    for i in range(search_pages):
        page = doc.loadPage(i)
        page_text = page.getText()
        # print(page_text)
        if keyword in page_text:
            num=1
            pattern = re.compile(keyword1, re.S)
            temp_list = pattern.findall(page_text)
            # print(333333333333333333333)
            # print(temp_list)
            result.extend(temp_list)
        else:
            if num == 1:
                num = i
            continue

    if len(result):
        # print(result[0])
        page = doc.loadPage(int(result[0][2])-1)
        # print(page.getText())
        fig_rect=page.searchFor(result[0][0][0:10])#直接根据目录匹配
        a=0
        if not len(fig_rect):#根据图表+数字匹配
            a=1
            fig_num_r = r'(图\s*表|表|图)(\s*\d+)'
            pattern = re.compile(fig_num_r)
            match=pattern.search(result[0][0])
            if match:
                fig_num=match.group()
                fig_rect=page.searchFor(fig_num)
                if not len(fig_rect):#根据图表+数字去掉空格匹配
                    a=2
                    # front = r'([图表]+\s*[图表]*\d+)(\s*[：.:]?\s*)(.+)'
                    fig_num1=re.sub('\s','',fig_num)
                    fig_rect=page.searchFor(fig_num1)
        if not len(fig_rect):#根据图表名的一部份匹配
            a=3
            name_r=r'[\u4e00-\u9fa5]{3,}'
            pattern1 = re.compile(name_r)
            name=pattern1.findall(result[0][0])
            if len(name):
                name_=name[0]
                for x in name:
                    if len(name_)<len(x):
                        name_=x
                fig_rect=page.searchFor(name_)
        if not len(fig_rect):
            flag=1
    doc.close()
    return result,num,flag

# 参数需要上一个函数处理完之后的目录列表
def catalog_list_grouping(list):
    dic = {}
    # split_keyword = r'\.+'
    for item in list:
        # pattern = re.compile(split_keyword)
        # temp_list = pattern.split(item)
        # strinfo = re.compile('\s+')
        # page = strinfo.sub('', temp_list[-1])
        page=item[2]
        page=page.strip()
        name=item[0]
        name=name.replace('\n','')
        name=name.rstrip()
        name=name.rstrip('.')
        if page in dic:
            dic[page].append(name)
        else:
            dic[page] = [name]

    return dic



if __name__ == '__main__':
    file_name = 'D:/20180815-兴业证券-商业航天行业研究：SpaceX以及低轨道小卫星星座启示录.pdf'
    lists,first_page,flag = catalog_extract(file_name)
    for x in lists:
        print(x[0],x[2],flag)
    # print(lists)
    dis = catalog_list_grouping(lists)
    # print(dis)
    # print(dis)
    # for key,value in dis.items():
    #     print(key,value)