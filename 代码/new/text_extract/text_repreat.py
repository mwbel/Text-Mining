#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz
import re

# 求出两个子串的共同子序列
def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return s1[p - mmax:p], mmax  # 返回最长子串及其长度


# 处理截取的重复数据
def deal_repeat(list):
    list_group = [[]]
    # 对整体的字符进行分组
    for item in list:
        list_temp = list_group[-1]
        if list_temp:
            if list_temp[0][5] == item[5]:
                list_group[-1].append(item)
            else:
                list_new = []
                list_new.append(item)
                list_group.append(list_new)
        else:
            list_new1 = []
            list_new1.append(item)
            list_group[-1] = list_new1

    # 对每一组进行分别处理
    result = []
    for group_item in list_group:
        length = len(group_item)
        str_temp = ''
        for i in range(length):
            str1 = group_item[i][4]
            str_common, length_com = find_lcsubstr(str_temp, str1)
            if length_com != 0:
                temp = str_temp[:-length_com]
                str_temp = temp + str1
            else:
                str_temp = str_temp + str1
        result.append(str_temp)
    return result


def deal_pdf_catalog(file_name):
    doc = fitz.open(file_name)
    keyword = '........'
    catalog_text = []
    for i in range(10):
        page = doc.loadPage(i)
        page_text = page.getText()
        if keyword in page_text:
            words = page.getTextWords()
            result = deal_repeat(words)
            catalog_text.extend(result)

    result = []
    keyword1 = r'\s*图\s*目\s*|\s*插\s*图\s*|\s*表\s*目\s*|\s*表\s*格\s*|\s*图\s*表'
    length = len(catalog_text)
    for j in range(length):
        if '.....' in catalog_text[j]:
            result.append(catalog_text[j])
        elif re.match(keyword1, catalog_text[j], re.I):
            break
    return result


if __name__ == '__main__':
    a = deal_pdf_catalog('D:/Study/工程项目/测试文件/999.pdf')
    for i in a:
        print(i)
