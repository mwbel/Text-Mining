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
def preprocess(path):
    '''
    在截取图片之前对数据进行预处理
    :param path:文件路径, pdf文件
    :return:分类后的文件路径（键是来源，值是文件路径）
    '''
    materialsource = []
    datasource = []
    source = []
    mkpath1 = path + "/资料来源"
    mkpath2 = path + "/数据来源"
    mkpath3 = path + "/来源"
    mkpath4 = path + "/未处理完成"
    pathdir = {"资料来源：":mkpath1, "数据来源：":mkpath2, "来源：":mkpath3}
    mkdir(mkpath1)
    mkdir(mkpath2)
    mkdir(mkpath3)
    mkdir(mkpath4)
    for file in os.listdir(path):
        # print(file)
        keywords1 = r'\s*资料来源：*'
        keywords2 = r'\s*数据来源：*'
        keywords3 = r'\s+来源：*'
        flag = True
        if file[-4:] == '.pdf':
            doc = fitz.open(os.path.join(path, file))
            page_count = doc.pageCount
            for i in range(1, page_count):
                page = doc.loadPage(i)
                page_text = page.getText()
                find1 = re.findall(keywords1, page_text)
                find2 = re.findall(keywords2, page_text)
                find3 = re.findall(keywords3, page_text) 
                if len(find1) and len(find2):
                    flag = False
                    break
                if len(find1) and len(find3):
                    flag = False
                    break
                if len(find2) and len(find3):
                    flag = False
                    break
                materialsource.extend(find1)
                datasource.extend(find2)
                source.extend(find3)
                # print(i)
                # print(len(materialsource))
                # print(datasource)
                # print(len(datasource))
                # print(len(source))
                
            doc.close()
            # print(materialsource)
            # print(len(materialsource))
            # print(datasource)
            # print(len(datasource))
            # print(source)
            # print(len(source))
            # print("______________________________________")
            if not flag:
                shutil.copy(os.path.join(path, file), os.path.join(mkpath4, file))
            else:
                if len(materialsource) and not len(source) and not len(datasource):
                    shutil.copy(os.path.join(path, file), os.path.join(mkpath1, file))
                elif len(datasource) and not len(source) and not len(materialsource):
                    shutil.copy(os.path.join(path, file), os.path.join(mkpath2, file))
                elif len(source) and not len(datasource) and not len(materialsource):
                    shutil.copy(os.path.join(path, file), os.path.join(mkpath3, file)) 
                else:
                    shutil.copy(os.path.join(path, file), os.path.join(mkpath4, file))   
            materialsource = []
            datasource = []
            source = []
    return pathdir 

path = "E:/项目/试运行/201808/需求4/处理完成/测试"
# file = ""
preprocess(path)