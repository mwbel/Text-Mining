#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz


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


def extract_title_content(file_name):
    doc = fitz.open(file_name)
    page = doc[0]
    d = page.getText("dict")
    
    # print(d)
    size1_max = 0.0
    result1 = []
    for i in range(len(d['blocks'])):
        if d['blocks'][i].__contains__('lines'):
            length1 = len(d['blocks'][i]['lines'])
            size_max = 0.0
            result = []
            for j in range(length1):
                if d['blocks'][i]['lines'][j].__contains__('spans'):
                    size = d['blocks'][i]['lines'][j]['spans'][0]['size']
                    text_list = []
                    for k in range(len(d['blocks'][i]['lines'][j]['spans'])):
                        text_list.append(d['blocks'][i]['lines'][j]['spans'][k]['text'])
                    text = ''.join(text_list)
                    if size == size_max:
                        result.append(text)
                    if size > size_max:
                        size_max = size
                        result.clear()
                        result.append(text)
                    # print(result)
            if size1_max < size_max:
                size1_max = size_max
                result1.clear()
                result1.append(result)
            if size1_max == size_max:
                result1.append(result)
    # print(size1_max, '', result1)

    return result1


def connect_title(list):
    temp_list = []
    for group_item in list:
        length = len(group_item)
        str_temp = ''
        for i in range(length):
            str1 = group_item[i]
            str_common, length_com = find_lcsubstr(str_temp, str1)
            if length_com != 0:
                temp = str_temp[:-length_com]
                str_temp = temp + str1
            else:
                str_temp = str_temp + str1
        temp_list.append(str_temp)
    # print(temp_list)
    final_str = ''
    for j in range(len(temp_list)):
        str2 = temp_list[j]
        str_common1, length_com1 = find_lcsubstr(final_str, str2)
        if length_com1 != 0:
            temp = final_str[:-length_com1]
            final_str = temp + str2
        else:
            final_str = final_str + str2
    return final_str


if __name__ == '__main__':
    list = extract_title_content('E:/项目/试运行/201808/需求4/处理完成/测试/测试/数据来源/20180806-广发证券-电子行业：光学行业研究专题二：从光学升级的三条路径看行业变革.pdf')
    s = connect_title(list)
    print(s)
    

