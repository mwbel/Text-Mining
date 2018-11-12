import os
import fitz
import re
import shutil
from operator import itemgetter 
from itertools import groupby

def mkdir(path):
    '''
    新建目录
    :param path:要创建的路径
    :return:
    '''
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

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

# def picname(i):
#     page = doc[i]
#     text=page.getText()
#     re_telephone = re.compile(r'图表 [0-9][^\.]*')
#     picname_list1=re_telephone.findall(text)
#     return picname_list1

# doc = fitz.open("E:\\项目\\试运行\\201808\\有目录\\新建文件夹\\20180801-方正证券-通信行业专题：正在加速来临的产业趋势之to B大时代.pdf")     # 打开文件
# page_num=doc.pageCount            # 页数

def image_extract(path):
    keywords = "........"
    for file in os.listdir(path):
        if file[-4:]==".pdf":
            mkpath = '/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/有目录/第一批/图片'
            mkpath = mkpath + file[:-4] + '/'
            mkdir(mkpath + '/' + file[:-4])
            doc = fitz.open(os.path.join(path, file))
            page_count = doc.pageCount
            picname_num = 0
            picname_list = []
            for i in range(10):
                page = doc.loadPage(i)
                page_text = page.getText()
                if keywords in page_text:
                    pattern = re.compile(r'图表 [0-9][^\.]*')
                    picname_list1 = pattern.findall(page_text)
                    picname_list.extend(picname_list1)
            # print(picname_list)
            for i in range(page_count):
                # page = doc[i]
                # links = page.getLinks()
                page = doc.loadPage(i)
                page_text = page.getText()
                # pic = page.searchFor("图表"|"图"|"表")
                pic = page.searchFor("图表")
                # data = page.searchFor("资料来源："|"数据来源："|"来源：")
                data = page.searchFor("资料来源：")
                # print(len(pic))
                # print(len(data))
                if len(pic) > len(data):#图表数多于资料来源
                    pic = pic[:len(data)-len(pic)]
                elif len(pic) < len(data):#资料来源多于图表数
                    for i in range(len(data)-len(pic)):
                        pic.insert(0, fitz.Rect(0, 0, 0, 0))

                if len(pic) != 0 and len(data) != 0 and len(pic) == len(data):
                    mat = fitz.Matrix(3, 3)                  # 缩放
                    page_ = page.rect                        # 页面大小
                    page_length = page_.x1                     #页面长
                    page_width = page_.y1                      #页面宽

                    # words = page.getTextWords()              #获取页面文字
                    # print(words)
                    pic1=[[]]
                    data1=[[]]
                    length=len(pic)                          #图表数
                    for i in range(length):                  #将图表按行分组
                        if i < (length-1):
                            if pic[i].y0==pic[i+1].y0:
                                pic1[-1].append(pic[i])
                                data1[-1].append(data[i])
                            else:
                                pic1[-1].append(pic[i])
                                pic1.append([])
                                data1[-1].append(data[i])
                                data1.append([])
                    pic1[-1].append(pic[i])
                    data1[-1].append(data[i])

                    picgroup_num=len(pic1)                  #图片组数


                    for i in range(picgroup_num):           #按组处理图片
                        for j in range(len(pic1[i])):
                            if j < len(pic1[i])-1:
                                clip = fitz.Rect(data1[i][j].x0-5, pic1[i][j].y0, data1[i][j+1].x0-18, data1[i][j].y1)
                                pix = page.getPixmap(matrix = mat, clip = clip, alpha = False)
                                # print(pix)
                                fn = picname_list[picname_num]+".png"
                                pix.writePNG(os.path.join(mkpath, fn))
                                picname_num = picname_num+1
                            else:
                                clip=fitz.Rect(data1[i][j].x0-5, pic1[i][j].y0, page_length-49, data1[i][j].y1)
                                pix = page.getPixmap(matrix = mat, clip = clip, alpha = False)
                                fn = picname_list[picname_num]+ ".png"
                                pix.writePNG(os.path.join(mkpath, fn))
                                picname_num = picname_num + 1
            doc.close()
            shutil.copy(os.path.join(path, file), os.path.join(mkpath, file))

image_extract("/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/有目录/第一批")