#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, os.path
import shutil
import os.path
import fitz
import re


# 创建目录
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # print(path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(path+' 目录已存在')
        return False


# 预处理PDF，先进行初次判断
def classify(path):
    path_list = []
    keywords = '.........'
    mkpath1 = path + '/处理完成/'
    mkpath2 = path + '/暂时无法处理/'
    mkdir(mkpath1)
    mkdir(mkpath2)
    for file in os.listdir(path.replace('\\', '/')):
        if file[-4:] == '.pdf':
            flag = False
            doc = fitz.open(os.path.join(path, file))
            # 会出现效率问题，但没有办法，格式种类太丰富
            pageCount = doc.pageCount
            for i in range(1, pageCount):
                page = doc.loadPage(i)
                page_text = page.getText()
                if keywords in page_text:
                    flag = True
                    break
            doc.close()
            if flag:
                file_dir = os.path.join(mkpath1, file[:-4])
                mkdir(file_dir)
                path_list.append(file_dir)
                shutil.copy(os.path.join(path, file), os.path.join(file_dir, file))
            else:
                shutil.copy(os.path.join(path, file), os.path.join(mkpath2, file))
    # 返回初步含有目录的PDF路径
    return path_list


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
    # for item_temp in list_group:
    #     # 对每一个分组的情况进行排序
    #     item_temp.sort(key=itemgetter(0, 6, 7))
    # 对每一组进行分别处理
    result = []
    for group_item in list_group:
        length = len(group_item)
        str_temp = ''
        for i in range(length):
            str1 = group_item[i][4]
            str_common, length_com = find_lcsubstr(str_temp, str1)
            if length_com > 1 and str_temp[-length_com:] == str_common and str1[:length_com] == str_common:
                temp = str_temp[:-length_com]
                str_temp = temp + str1
            else:
                str_temp = str_temp + str1
            # print(str_temp)
        result.append(str_temp + '\n')
    return result


# 获取目录所在页的文本内容
def deal_pdf_catalog(file_name):
    doc = fitz.open(file_name)
    pageCount = doc.pageCount
    keyword = '........'
    catalog_text = []
    for i in range(1, pageCount):
        page = doc.loadPage(i)
        page_text = page.getText()
        if keyword in page_text:
            words = page.getTextWords()
            # for i in words:
            #     print(i)
            result = deal_repeat(words)
            catalog_text.extend(result)
    doc.close()
    return catalog_text


def first_write_catalog(path_list):
    for path in path_list:
        for file in os.listdir(path):
            file_name = os.path.join(path, file).replace('\\', '/')
            print(file_name)
            if file_name[-4:] == '.pdf':
                result = deal_pdf_catalog(file_name)
                pos = file.index('.')
                last_file_name = os.path.join(path, file[:pos + 1] + 'txt')
                with open(last_file_name, 'w', encoding='utf8') as f:
                    f.writelines(result)
    return path_list


def deal_catalog(path_list):
    '''
    将提取的目录进行处理，把内容目录和图表目录分开
    :param file_list: pdf文件路径列
    :return:
     '''
    keyword = r'.*\s*目\s*录\s*'
    keyword1 = '.....'
    keyword2 = r'：|;|、|\.'
    keyword4 = r'\s*图\s*表\s*'
    keyword5 = r'\d*\.\d*'
    keyword6 = r'\s*图\s*目\s*|\s*插\s*图\s*|\s*表\s*目\s*|\s*表\s*格\s*'
    keyword_not = r'本研究|证监许可|请仔细阅读|请阅读|请务必阅读|行业深度|行业：十年涅|资料来源|中金公司研|计算机行业：在技术|旅游深度报告|油服行业：油|专题报告：'
    for path in path_list:
        for file in os.listdir(path):
            if file[-4:] == '.txt':
                # print(file_name)
                file_name1 = os.path.join(path, file)
                fro = open(file_name1, "r", encoding='utf8')
                filelist = fro.readlines()
                result = []
                for fileline in filelist:
                    # print(fileline,len(fileline))
                    # print(re.match(keyword, fileline, re.I))
                    if (re.match(keyword, fileline, re.I) or re.match(keyword4, fileline,
                                                                      re.I)) and '..' not in fileline:
                        result.append('\n')
                        result.append(fileline + '\n')
                        result.append('\n')
                    if keyword1 in fileline or re.search(keyword2, fileline, re.I) or re.match(keyword5, fileline,
                                                                                               re.I):
                        if re.search(keyword_not, fileline, re.I):
                            continue
                        else:
                            result.append(fileline)
                    else:
                        continue
                fro.close()
                count = 0
                for deal in result:
                    if (re.match(keyword4, deal, re.I) or re.match(keyword6, deal, re.I)) and '..' not in deal:
                        break
                    count += 1
                # print(count)
                pos = file.index('.')
                newname = file[:pos + 1] + 'pdf' + '\n'
                list1 = [newname] + result[0:count]
                list2 = result[count:]
                List_2_end = []
                if len(list2) != 0:
                    list_head = []
                    list_head.append(newname + '\n')
                    list_head.append('\n')
                    List_2_end = list_head + list2

                os.remove(file_name1)  # 删除原目录
                last_file_name = os.path.join(path, '目录-' + file)
                last_file_name1 = os.path.join(path, '图表目录-' + file)

                with open(last_file_name, 'w', encoding='utf8') as f:
                    f.writelines(list1)
                if len(List_2_end) != 0:
                    with open(last_file_name1, 'w', encoding='utf8') as f:
                        f.writelines(List_2_end)


if __name__ == '__main__':
    # 写入要测试的pdf在文件夹，之后对目录进行筛选和提取
    # 一定要用'/'
    rootdir = 'D:/Study/工程项目/测试文件'
    deal_path = classify(rootdir)
    catalog_path = first_write_catalog(deal_path)
    deal_catalog(catalog_path)
