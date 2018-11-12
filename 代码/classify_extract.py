import fitz
import os
import shutil
from source_classify import *

def test_file(path,name_lists):
    # if not os.path.exists(os.path.join(path,'represents')):
    #     os.makedirs(os.path.join(path,'represents'))
    for name in os.listdir(path):
        if name.endswith('.pdf'):
            for name_list in name_lists:
                output_path = os.path.join(path, name_list)
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                if name_list in name:
                    shutil.copy(os.path.join(path,name), output_path)
                    # shutil.copy(os.path.join(path,name), os.path.join(path,'represents'))

def classify_extract(path):
    doc = fitz.open(path)
    page_count = doc.pageCount
    # print(page_count)
    con_key = ".........."              # 判断此页是否是目录页的关键字
    count = 1
    head_name = '图表'                  # 表头关键字 
    name_rects = []
    source_rects = []
    for i in range(1,page_count):
        name_rects_page = []
        source_rects_page = []
        page = doc.loadPage(i)
        page_text = page.getText()
        # toc = doc.getToC()
        # print(toc)
        if con_key in page_text:
            # print(i)
            continue
        for j in range(10):
            name = head_name + str(count)
            name_rect = page.searchFor(name)
            # print(name_rect,end = '')
            if len(name_rect):
                count = count+1
                name_rects_page.append(name_rect[0])
            else:
                break
        # print(name_rects_page)
        source_rects_page = page.searchFor('来源')
        # print(source_rects_page)
        if len(source_rects_page):
            for rect in source_rects_page:
                source_rects.append(rect)
        if len(name_rects_page):
            for rect in source_rects_page:
                name_rects.append(rect)
        # print(i)
    print(len(source_rects))
    print(source_rects)
    print(len(name_rects))
    print(name_rects)   
    doc.close()


if __name__=='__main__':
    # classify_extract('E:/20180801-广证恒生-【新型制剂系列专题】ALZA：载药技术先驱的崛起与启示.pdf')
    name_lists = ['民生', '太平洋', '国金', '华创', '申万宏源', '兴业', '中信', '方正', '中银国际', '安信', '广发', '平安']
    test_file('E:/项目/试运行/201808', name_lists)



