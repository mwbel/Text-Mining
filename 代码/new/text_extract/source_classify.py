import os
import shutil
import fitz
import re
# from zhengze import mkdir

def mkdir(path):
    '''
    新建目录
    :param path:要创建的路径
    :return:
    '''
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
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建
        return False

# 对文件进行预处理，分成资料来源，数据来源，来源三种情况
def preprocess(path, file):
    '''
    在截取图片之前对数据进行预处理
    :param path: 文件路径, 
    :file:pdf文件
    :return: 字符串："资料来源" 或者 "数据来源" 或者 "来源" 或者 "未处理完成"
    '''
    materialsource = []
    datasource = []
    source = []
    keywords1 = r'\s*资料来源*'
    keywords2 = r'\s*数据来源*'
    keywords3 = r'\s+来源*'
    keywords4 = r'\s+料来源*'
    flag = True                     # 标记是否在同一页同时出现了'资料来源'、'数据来源'、'来源'中的两个或以上
    if file.endswith('.pdf'):
        doc = fitz.open(os.path.join(path, file))
        page_count = doc.pageCount
        for i in range(1, page_count):
            page = doc.loadPage(i)
            page_text = page.getText()
            find1 = re.findall(keywords1, page_text)
            find2 = re.findall(keywords2, page_text)
            find3 = re.findall(keywords3, page_text) 
            find4 = re.findall(keywords4, page_text) 
            if len(find1) and len(find2):
                flag = False
                break
            if len(find1) and len(find3):
                flag = False
                break
            if len(find2) and len(find3):
                flag = False
                break
            if len(find1) and len(find4):# 表示同一页既出现了'资料来源'又出现了'料来源'
                flag = False
                break
            materialsource.extend(find1)
            datasource.extend(find2)
            source.extend(find3)   
        doc.close()
        if not flag:
            return "未处理完成"
        else:
            if len(materialsource) and not len(source) and not len(datasource):
                return "资料来源"
            elif len(datasource) and not len(source) and not len(materialsource):
                return "数据来源"
            elif len(source) and not len(datasource) and not len(materialsource):
                return "来源"
            else:
                return "未处理完成"  

# path = "E:/项目/试运行/201808/需求4/处理完成/测试/新建文件夹"
# file = "20180801-兴业证券-医药生物：品种引进大潮起，License-in模式方兴未艾.pdf"
# s = preprocess(path, file)
# print(s)