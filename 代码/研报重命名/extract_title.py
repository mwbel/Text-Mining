#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz
import re
import os


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


def extract_title_content(page, kind):
    d = page.getText("dict")
    print(d)
    # 获取每个小块用于文字拼接和处理重复
    blocks_text = page.getTextWords()
    for o in blocks_text:
        print(o)
    # 获取每一行的块号，用于获取标题所在的块号，进而提取副标题
    blocks = page.getTextBlocks()
    print('输出块号：')
    for l in blocks:
        print(l)
    size1_max = 0.0
    result1 = []
    for i in range(len(d['blocks'])):
        if d['blocks'][i].__contains__('lines'):
            length1 = len(d['blocks'][i]['lines'])
            size_max = 0.0
            result = []
            for j in range(length1):
                if d['blocks'][i]['lines'][j].__contains__('spans'):
                    length2 = len(d['blocks'][i]['lines'][j]['spans'])
                    # print('字体大小', size, '，位置', d['blocks'][i]['lines'][j]['bbox'])
                    text_list = []
                    location = d['blocks'][i]['lines'][j]['bbox']
                    if kind == '中信证券':
                        if location[0] > 380:
                            continue
                    if kind == '方正证券':
                        if location[2] < 240:
                            continue
                    if kind == '华创证券':
                        if location[0] > 380:
                            continue
                    if kind == '国金证券':
                        if location[1] < 100:
                            continue
                    if kind == '中银国际证券':
                        if location[2] < 210:
                            continue
                    if kind == '安信证券':
                        if location[0] > 400:
                            continue
                    if kind == '中泰证券':
                        if location[2] < 170:
                            continue
                    if kind == '东北证券':
                        if location[0] > 350:
                            continue
                    if kind == '联讯证券':
                        if location[0] < 200:
                            continue
                    if kind == '山西证券':
                        if location[0] < 180:
                            continue
                    if kind == '东兴证券':
                        if location[0] < 30:
                            continue
                    if kind == '致富證券' or kind == '致富集團':
                        if location[0] > 480:
                            continue
                    if kind == '广证恒生':
                        if location[1] > 200:
                            continue
                        if location[0] > 410:
                            continue
                    if kind == '财富证券':
                        if location[1] < 30:
                            continue
                        if location[0] < 155:
                            continue
                    if kind == '万联证券':
                        if location[0] > 430:
                            continue
                    if kind == '中信建投证券':
                        if location[0] > 430:
                            continue
                    if kind == '华金证券':
                        if location[0] > 430:
                            continue
                    size = 0
                    for k in range(length2):
                        temp_size = d['blocks'][i]['lines'][j]['spans'][k]['size']
                        temp = d['blocks'][i]['lines'][j]['spans'][k]['text']
                        if re.match(r'^\s*$', temp, re.I):
                            continue
                        if temp_size - size >= 0.5:
                            size = temp_size
                        text_list.append(temp)
                    print("每一行的结果：")
                    print(text_list)
                    text = ''.join(text_list)
                    if '推荐' in text:
                        continue
                    if re.match(r'^\s*$', text, re.I):
                        continue
                    if size == size_max:
                        result.append(text)
                    elif size - size_max > 0.5:
                        size_max = size
                        result.clear()
                        result.append(text)
            print(size_max, '最大值', result)
            print('----------------------')
            if size_max - size1_max > 0.5:
                size1_max = size_max
                result1.clear()
                result1.append(result)
            elif size1_max == size_max:
                result1.append(result)
    print(size1_max, '  ', result1)

    # 进一步获取和判断是否存在副标题
    result2 = []
    if kind == '财通证券' or kind == '招银国际' or kind == '天风证券' or kind == '招商证券' or kind == '华金证券':
        result2 = extract_title_content_special(d, kind, result1)
        print('返回结果', result1, result2)
        return result1, result2
    if kind == '太平洋证券' or kind == '国金证券':
        st = ' '.join(result1[0])
    else:
        if kind == '国海证券':
            st = ' '.join(result1[-2])
            result1 = result1[:-1]
        else:
            st = ' '.join(result1[-1])
    # print(st)

    blocks_length = len(blocks)
    for item in range(blocks_length):
        if st in blocks[item][4]:
            print("主标题所在块号为", blocks[item][5])
            if item + 1 == blocks_length:
                break
            else:
                subtitle = blocks[item + 1][4]
                if re.match(r'^\s*$', subtitle, re.I):
                    break
                else:
                    company_name = ['红杉资本', '中银国际证券', '广发证券', '华泰证券', '西部证券', '中国国际金融', '国盛证券', '开源证券']
                    if kind not in company_name:
                        if not re.match(r'.*\s*[—|-|―|-|─]+', subtitle, re.I):
                            break
                        else:
                            if kind == '中原证券':
                                if not re.match(r'\s*[—|-|―|-|─]+', subtitle, re.I):
                                    break
                            if kind == '中商产业研究院':
                                if not re.match(r'[^\d]\s*[—|-|―|-|─]+', subtitle, re.I):
                                    break
                    if kind == '民生证券':
                        if blocks[item + 1][0] > 400:
                            break
                    result2 = extract_blocks_text(blocks_text, blocks[item][5] + 1, kind)
    print(result1, '-----', result2)
    if kind == '太平洋证券':
        result1 = result1[0]
    else:
        pass
    return result1, result2


# 特殊提取副标题的函数
def extract_title_content_special(d, kind, pre_result):
    size1_max = 0.0
    result1 = []
    for i in range(len(d['blocks'])):
        if d['blocks'][i].__contains__('lines'):
            length1 = len(d['blocks'][i]['lines'])
            size_max = 0.0
            result = []
            for j in range(length1):
                if d['blocks'][i]['lines'][j].__contains__('spans'):
                    length2 = len(d['blocks'][i]['lines'][j]['spans'])
                    # size = d['blocks'][i]['lines'][j]['spans'][0]['size']
                    # print('字体大小', size, '，位置', d['blocks'][i]['lines'][j]['bbox'])
                    text_list = []
                    location = d['blocks'][i]['lines'][j]['bbox']
                    if kind == '财通证券':
                        if location[1] < 90 or location[0] < 220:
                            continue
                    if kind == '招银国际':
                        if location[3] < 100:
                            continue
                    if kind == '天风证券':
                        if location[1] < 100:
                            continue
                    if kind == '华金证券':
                        if location[0] > 430:
                            continue
                    size = 0
                    for k in range(length2):
                        temp_size = d['blocks'][i]['lines'][j]['spans'][k]['size']
                        temp = d['blocks'][i]['lines'][j]['spans'][k]['text']
                        if re.match(r'^\s*$', temp, re.I):
                            continue
                        if temp_size - size >= 0.5:
                            size = temp_size
                        text_list.append(temp)
                    text = ''.join(text_list)
                    if '推荐' in text or '中性' in text:
                        continue
                    flag = False
                    for temp_item in pre_result:
                        if text in temp_item:
                            flag = True
                    if flag:
                        continue
                    if re.match(r'^\s*$', text, re.I):
                        continue
                    if size == size_max:
                        result.append(text)
                    elif size - size_max > 0.5:
                        size_max = size
                        result.clear()
                        result.append(text)
            if size_max - size1_max > 0.5:
                size1_max = size_max
                result1.clear()
                result1.append(result)
            elif size1_max == size_max:
                result1.append(result)
    # print(size1_max, '  ', result1)
    return result1


# getTextBlocks所对应的块号和getTextWords的行号相对应，需要重新编写内容
def extract_blocks_text(list, num, kind):
    result = []
    for item in list:
        if item[5] == num:
            if kind == '申万宏源证券':
                if item[2] < 100:
                    continue
            if kind == '新时代证券':
                if item[0] > 470:
                    continue
            if kind == '山西证券':
                if item[0] > 530:
                    continue
            if kind == '中国国际金融':
                if item[1] > 170:
                    continue
            if kind == '万联证券':
                if item[0] > 430:
                    continue
            result.append(item[4])
    return result


def connect_title(list):
    temp_list = []
    list_num = len(list)
    if list_num == 0:
        return ''
    if list_num == 1 and isinstance(list[0], str):
        return list[0]
    else:
        if isinstance(list[0], str):
            temp_list = list
        else:
            for group_item in list:
                length = len(group_item)
                str_temp = ''
                for i in range(length):
                    str1 = group_item[i]
                    str_common, length_com = find_lcsubstr(str_temp, str1)
                    if length_com > 1 and str_temp[-length_com:] == str_common and str1[:length_com] == str_common:
                        temp = str_temp[:-length_com]
                        str_temp = temp + str1
                    else:
                        if str1 in str_temp:
                            continue
                        else:
                            str_temp = str_temp + str1
                    # print('1111111111', str_temp)
                temp_list.append(str_temp)
        final_str = ''
        for j in range(len(temp_list)):
            str2 = temp_list[j]
            str_common1, length_com1 = find_lcsubstr(final_str, str2)
            if length_com1 > 1 and final_str[-length_com1:] == str_common1 and str2[:length_com1] == str_common1:
                temp = final_str[:-length_com1]
                final_str = temp + str2
            else:
                # 需要考虑后一个字符出现在前一段字符中，需要处理不进行连接
                if str2 in final_str:
                    continue
                else:
                    final_str = final_str + str2
            print(final_str)
        return final_str


# 进行简单的去重
def connect_date(list):
    final_str = ''
    for j in range(len(list)):
        str1 = list[j]
        str_common1, length_com1 = find_lcsubstr(final_str, str1)
        if length_com1 >= 1:
            if final_str[-length_com1:] == str_common1 and str1[:length_com1] == str_common1:
                temp = final_str[:-length_com1]
                final_str = temp + str1
            else:
                final_str = final_str + str1
        else:
            # 需要考虑后一个字符出现在前一段字符中，需要处理不进行连接
            if str1 in final_str:
                continue
            else:
                final_str = final_str + str1
    return final_str


# 对页面进行简单重新排版
def re_composing(page):
    list = []
    blocks = page.getTextWords()
    if len(blocks) == 0:
        return ''
    length = len(blocks)
    # 先放入第一个元素
    list.append(blocks[0][4])
    result = ''
    for i in range(1, length):
        last = blocks[i - 1]
        curr = blocks[i]
        # print('上一块:', last[4], '-----当前块:', curr[4])
        if last[5] == curr[5]:
            list.append(curr[4])
        else:
            # temp = ''.join(list)
            temp = connect_date(list)
            # print('每一行---', temp)
            result = result + temp + '\n'
            list.clear()
            list.append(curr[4])
    # 存放最后一行的数据
    # temp = ''.join(list)
    temp = connect_date(list)
    result = result + temp + '\n'
    return result


# 进行日期提取
def extract_date_temp(page, create_date, kind):
    # 获取文件的创建时间
    # print(create_date)
    content = re_composing(page)
    # print(content)
    # 致富证券要重新考虑
    if kind == '致富證券' or kind == '致富集團':
        date_format = r'(\d{1,2}\s*[-|日|-|\.|/]\s*\d{1,2}\s*[-|月|-|\.|/]\s*\d{4})'
        mat = re.findall(date_format, content)
        temp_result = []
        for one in mat:
            temp = re.split(r'[-|年|-|\.|/]', one)
            temp = list(reversed(temp))
            temp_result.append('/'.join(temp))
        mat.clear()
        mat = temp_result
    else:
        date_format = r'(\d{4}\s*[-|年|-|\.|/]\s*\d{1,2}\s*[-|月|-|\.|/]\s*\d{1,2})'
        mat = re.findall(date_format, content)
    # print(mat)
    # 要对致富证券进行特殊处理

    deal_list = []
    for item in mat:
        first = re.sub(r'\s*', '', item)
        second = re.sub(r'年|月|\.|/', '-', first)
        temp_list = second.split('-')
        third = []
        for one in temp_list:
            if len(one) < 2:
                third.append('0' + one)
            else:
                third.append(one)
        forth = ''.join(third)
        deal_list.append(forth)
    result = []
    # 删除不可能项
    if len(deal_list) > 1:
        for every in deal_list:
            if (int(every) - int(create_date)) > 3:
                continue
            else:
                result.append(every)
    else:
        result = deal_list
    result.sort(reverse=True)
    if len(result) < 1:
        return create_date
    else:
        return result[0]


def search_company(text):
    list = []
    with open(r'券商名称', 'r', encoding='utf-8') as f:
        temp = f.readlines()
    for item in temp:
        list.append(item.strip('\n'))
    length = len(list)
    num = []
    for i in range(length):
        str_company = list[i]
        if len(str_company) <= 4:
            res = re.findall(str_company[:-1], text)
        else:
            res = re.findall(str_company[:-2], text)
        weight = (len(str_company) ** 2) * len(res)
        num.append(weight)
    max_num = max(num)
    if max_num == 0:
        return ''
    else:
        return list[num.index(max_num)]


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def title_extract(file_path):
    folder_name = file_path + '/重新命名的研报'
    fail_name = file_path + '/命名失败的研报'
    mkdir(folder_name)
    mkdir(fail_name)
    for file in os.listdir(file_path):
        if file[-4:] == '.pdf':
            doc = fitz.open(file_path + '/' + file)
            try:
                page = doc[0]
                page_count = doc.pageCount
                content = ''
                if page_count <= 3:
                    page_company = doc[page_count - 1]
                    content = page_company.getText()
                # 获取最后5页的内容
                else:
                    for i in range(page_count - 4, page_count):
                        page_company = doc[i]
                        content = content + page_company.getText()
                # 获取证券公司的姓名
                company = search_company(content)
                print('------------', company)
                # 获取证券的时间
                create_date = doc.metadata['creationDate']
                if create_date is None:
                    create_date = []
                date = extract_date_temp(page, create_date[2:10], company)
                # 获取证券公司的标题
                list1, list2 = extract_title_content(page, company)
                print(len(list2))
                # 过滤没有用的子标题
                if len(list2) > 10:
                    list2 = []
                print(list1)
                title1 = connect_title(list1)
                title2 = connect_title(list2)
                if title2 in title1:
                    title = title1.strip().replace(' ', '')
                else:
                    title = title1.strip().replace(' ', '') + ' ' + title2.strip().replace(' ', '')
                # print(title1+'-----'+title2)
                original_name = os.path.basename(doc.name)
                last_fail_name = fail_name + '/' + original_name
                # 处理没有提取成功的文件
                if date != '' and company != '' and title != '':
                    title = date + '-' + company + '-' + title + '-' + str(page_count) + '页.pdf'
                    # 处理非法字符
                    re_str = r"[\/\\\:\*\?\"\<\>\|]"
                    new_title = re.sub(re_str, '-', title)
                    last_name = folder_name + '/' + new_title
                    doc.save(last_name)
                else:
                    doc.save(last_fail_name)
                doc.close()
            except:
                doc.save(last_fail_name)


if __name__ == '__main__':
    # 填入要重命名的文件的目录地址
    # 该代码要和券商名称文件在一个文件夹下
    title_extract('D:/Study/工程项目/测试文件71')
