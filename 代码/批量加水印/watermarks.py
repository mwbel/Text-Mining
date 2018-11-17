#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fitz
import numpy as np
import math
import os


def add_watermarks(file_path, file_name, img, img1):
    doc = fitz.open(file_name)
    pix = fitz.Pixmap(img)
    pix1 = fitz.Pixmap(img1)
    # 水印大小
    img_width = pix.width
    img_height = pix.height
    # logo的大小
    img_width1 = pix1.width
    img_height1 = pix1.height
    page_num = doc.pageCount
    for i in range(page_num):
        page = doc[i]
        # 当前页面的大小
        page_width = page.rect.x1
        page_height = page.rect.y1
        # 加上文字水印
        font_height = 40
        font_width = 220
        font_rect = fitz.Rect(page.rect.x1 - font_width, page_height - font_height, page.rect.x1, page_height)
        link_rect = fitz.Rect(page.rect.x1 - font_width, page_height - font_height, page.rect.x1, page_height)
        link_rect1 = fitz.Rect(page_width - img_width1, 0, page_width, img_height1)
        watermarks_link = {'kind': 2, 'xref': i, 'from': link_rect, 'uri': 'http://www.767stock.com'}
        watermarks_link1 = {'kind': 2, 'xref': i + 1, 'from': link_rect1, 'uri': 'http://www.767stock.com'}
        page.insertLink(watermarks_link)
        page.insertLink(watermarks_link1)
        page.insertTextbox(font_rect, 'www.767stock.com', fontsize=25, fontname='Helvetica', color=(0.6, 0.6, 0.6))
        # 加上图片水印
        random_x_list = []
        random_y_list = []
        scale_list = []
        num = 2
        for i in range(num):
            random_x = int(np.random.rand() * (page_width - 50))
            random_y = int(np.random.rand() * (page_height - 50))
            scale = math.ceil(np.random.rand() * 3) + 0.5
            random_x_list.append(random_x)
            random_y_list.append(random_y)
            scale_list.append(scale)
        # 图像缩放系数
        for j in range(num):
            x = random_x_list[j]
            y = random_y_list[j]
            s = scale_list[j]
            image_rect = fitz.Rect(x / s, y / s, (x + img_width) / s, (y + img_height) / s)
            page.insertImage(image_rect, pixmap=pix)

        image_rect1 = fitz.Rect(page_width - img_width1, 0, page_width, img_height1)
        page.insertImage(image_rect1, pixmap=pix1)
        last_file_name = file_path + '/加完水印文件/' + os.path.basename(file_name) + '.pdf'
        # 测试方法，用来消除超链接的边框黑线
        allLinks = page.getLinks()  # allLinks is all links on thisPage
        for thisLink in allLinks:
            xrefValue = thisLink["xref"]
            if xrefValue == 0:
                continue
            s = doc._getXrefString(xrefValue)
            s = s[:-2] + "/BS<</W 0>>>>"
            doc._updateObject(xrefValue, s)
    doc.save(last_file_name, deflate=True)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def batch_add_watermarks(file_path):
    folder_name = file_path + '/加完水印文件'
    mkdir(folder_name)
    for file in os.listdir(file_path):
        if file[-4:] == '.pdf':
            file_name = file_path + '/' + file
            print(file)
            add_watermarks(file_path, file_name, '123.png', 'watermark_logo.jpg')


if __name__ == '__main__':
    # 传入要批量加水印的文件夹
    batch_add_watermarks('D:/Study/工程项目/测试文件')
