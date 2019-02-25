#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz
import json
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


def get_file_links(file_name):
    doc = fitz.open(file_name)
    page_num = doc.pageCount
    # 遍历每一个页码
    res_inform = []
    keywords = '.........'
    for i in range(page_num):
        page = doc[i]
        content = page.getText()
        if keywords not in content:
            continue
        all_links = page.getLinks()
        if len(all_links) == 0:
            continue
        # 获取pdf中的块
        blocks = page.getTextBlocks()
        for one in blocks:
            print(one)
        for j in all_links:
            kind = j['kind']
            if kind != 1:
                continue
            else:
                del_one = {}
                from_position = j['from'][0:]
                to_page = j['page']
                to_point = j['to'][0:]
                # del_one['position'] = from_position
                del_one['page'] = to_page + 1
                del_one['point'] = to_point
                width = doc[to_page].rect.y1
                del_one['top'] = width - to_point[1]
                # print('页面宽度---', width)
                chapter_content = []
                for one in blocks:
                    # print(one)
                    count = 0
                    for t in range(4):
                        if abs(one[t] - from_position[t]) > 11:
                            count += 1
                    if count < 2:
                        chapter_content.append(one[4])
                # print(chapter_content)
                del_one['text'] = chapter_content
                res_inform.append(del_one)
    rel_result = []
    max_page = 0
    pre_page = 0
    for item in res_inform:
        current = item['page']
        if max_page <= current and pre_page <= current:
            max_page = current
            rel_result.append(item)
            print(item)
        else:
            break
        pre_page = current
    return rel_result


def batch_process(folder_path):
    mkpath1 = folder_path + '/处理完成/'
    mkpath2 = folder_path + '/暂时无法处理/'
    mkdir(mkpath1)
    mkdir(mkpath2)
    for file in os.listdir(folder_path.replace('\\', '/')):
        if file[-4:] == '.pdf':
            print(file)
            source_file = os.path.join(folder_path, file)
            res = get_file_links(source_file)
            if len(res) == 0:
                shutil.copy(os.path.join(folder_path, file), os.path.join(mkpath2, file))
            else:
                file_dir = os.path.join(mkpath1, file[:-4])
                mkdir(file_dir)
                shutil.copy(os.path.join(folder_path, file), os.path.join(file_dir, file))
                file_name = os.path.basename(file)[:-4]
                new_name = '章节段落位置信息-' + file_name
                last_file_path = os.path.join(file_dir, new_name) + '.txt'
                res_str = []
                for item in res:
                    res_str.append(json.dumps(item, ensure_ascii=False) + '\n')
                with open(last_file_path, 'w', encoding='utf8') as f:
                    f.writelines(res_str)


if __name__ == '__main__':
    # 测试获取单个文件的段落信息
    # get_file_links('D:/OneDrive/OneDrive - stu.ecnu.edu.cn/Study/工程项目/测试文件1/20180816-民生证券-通信行业：5G频谱即将发放，带来产业全新机遇.pdf')
    # 用于批量处理获取pdf相关段落位置信息
    # 传入要处理的文件夹地址
    batch_process('D:/OneDrive/OneDrive - stu.ecnu.edu.cn/Study/工程项目/测试文件')
