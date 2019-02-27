#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz
import operator
import re
import os
import shutil


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


def validateTitle(title):
    '''
    将图表名中非法字符替换为下划线(_)
    参数:
        title:原图表名
    返回:
        new_title:替换后的图表名
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title.replace('\n', '')


def get_image_from_content(file_name, out_path, use_title=True):
    # 默认情况下是利用标题进行搜索和截取
    # 此时 use_title = True,想进行全文搜索需要设置为False

    doc = fitz.open(file_name)
    page_num = doc.pageCount
    location_list = []
    image_list = []
    for i in range(page_num):
        page = doc[i]
        content = page.getText()
        blocks = page.getTextBlocks()
        # 对数据进行简单的处理
        blocks_round = []
        for one in blocks:
            temp = []
            for j in range(4):
                temp.append(int(one[j]))
            temp.append(one[4])
            blocks_round.append(temp)
        # 根据纵坐标和横坐标进行排序
        blocks_sorted_y_x = sorted(blocks_round, key=operator.itemgetter(1, 0), reverse=False)
        # 添加关键词
        key_list = []
        with open(r'关键词', 'r', encoding='utf-8') as f:
            temp = f.readlines()
        for item in temp:
            key_list.append(item.strip('\n'))

        # print('-----------------------')
        # for item in blocks_sorted_y_x:
        #     print(item)
        if use_title:
            title_list = blocks_sorted_y_x[:3]
        else:
            title_list = blocks_sorted_y_x
        title_content = []
        for content in title_list:
            title_content.append(content[4])
        # 进行页面的匹配和截取
        # 首先获取前3行作为标题搜索的判断内容
        # 并保存相关位置信息
        flag = False
        # print(key_list)
        # print(title_content)
        for key in key_list:
            if key in ''.join(title_content):
                flag = True
        if flag:
            image_name = validateTitle(title_content[0]) + '.png'
            page.getPixmap().writePNG(os.path.join(out_path, image_name))
            position = image_name + '    ||page' + str(page.number + 1)
            if image_name not in image_list:
                image_list.append(image_name)
                location_list.append(position + '\n')

    return location_list


# 进行批量处理
def deal_lots_pdf(folder_path, use_title=True):
    mkpath1 = folder_path + '/处理完成/'
    mkpath2 = folder_path + '/暂时无法处理/'
    mkdir(mkpath1)
    mkdir(mkpath2)
    for file in os.listdir(folder_path):
        file_new = file.replace(' ', '')
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, file_new))
    for file in os.listdir(folder_path):
        if file[-4:] == '.pdf':
            print(file)
            source_file = os.path.join(mkpath1, file)
            # print(source_file)
            out_path = source_file[:-4]
            mkdir(out_path)
            shutil.copy(os.path.join(folder_path, file), os.path.join(out_path, file))
            res = get_image_from_content(os.path.join(folder_path, file), out_path, use_title)
            if len(res) == 0:
                shutil.move(out_path, os.path.join(mkpath2))
            else:
                # 对截取图片的位置信息进行输出
                file_name = os.path.basename(file)[:-4]
                new_name = '图片位置信息-' + file_name
                last_file_path = os.path.join(out_path, new_name) + '.txt'
                print(last_file_path)
                with open(last_file_path, 'w', encoding='utf8') as f:
                    f.writelines(res)


if __name__ == '__main__':
    # 第一参数是要处理的文件夹
    # 第二参数是选择搜索方式 default = True , True时按照标题进行搜索，False时按照全文进行搜索
    # 需要和 ‘关键字’文件配合使用，且要放在同一位置下
    deal_lots_pdf('D:/OneDrive/OneDrive - stu.ecnu.edu.cn/Study/工程项目/测试文件4', False)
