import fitz
import os
import shutil
from source_classify import *

def classify_file(path,name_lists):
    name_lists = list(tuple(name_lists))
    for file in os.listdir(path):
        if file.endswith('.pdf'):
            name = file.split('-')
            print(name)
            for name_list in name_lists:
                output_path = os.path.join(path,name_list)
                if len(name) == 1 and name_list == name[0]:
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    shutil.move(os.path.join(path,file), output_path)
                elif len(name) >1 and (name_list == name[0] or name_list == name[1] or name_list == name[2]):
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    shutil.move(os.path.join(path,file), output_path)
                else:
                    continue
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
    # name_lists1 = ['民生', '太平洋', '国金', '华创', '申万宏源', '兴业', '中信', '方正', '中银国际', '安信', '广发', '平安']

    # other_name = ['财达证券', '财富证券', '财通证券', '长城国瑞证券', '长城证券', '长江证券', '川财证券', '大通证券',
    #  '大同证券', '德邦证券', '第一创业证券',  '东方花旗证券', '东海证券', '东莞证券', '东兴证券', '东亚前海证券', '东证融汇证券', '方正证券',
    #  '高盛高华证券','广州证券', '国都证券', '国海证券',  '国开证券', '国联证券', '国融证券',
    #  '国元证券', '恒泰长财证券', '恒泰证券', '红塔证券', '宏信证券', '华安证券', '华宝证券', '华创证券', '华福证券', '华金证券', '华菁证券', '华林证券', '华龙证券',
    #  '华融证券', '华泰联合证券', '华泰证券', '华西证券', '华鑫证券', '华英证券', '汇丰前海证券', '江海证券', '金通证券', '金元证券', '九州证券', '开源证券', '联储证券', '联讯证券',
    #   '摩根士丹利华鑫证券', '南京证券',  '瑞信方正证券', '瑞银证券', '申港证券', '世纪证券', '首创证券',  '万和证券', '万联证券', '网信证券', '五矿证券', '西部证券', '西藏东方财富证券', '西南证券', '湘财证券', '新时代证券',  '兴证证券',
    #  '银河金汇证券', '银泰证券', '英大证券', '招商证券', '招商证券', '浙商证券', '中德证券', '中国国际金融', '中国民族证券', '中国中投证券', '中航证券', '中山证券',
    #   '中天证券', '中天国富证券', '中邮证券', '中原证券','爱建证券','渤海证券','财达证券','财富证券','川财证券','国都证券','国元证券','华融证券','交银国际证券','开源证券','农银国际证券','群益证券','万联证券','西南证券','浙商证券','中邮证券','中原证券']

    name_lists = [ '安信证券','东北证券', '东方证券', '东吴证券','东兴证券','光大证券', '广发证券', '广证恒生', '国金证券', '国盛证券', '国泰君安','东方财富','华泰证券','华金证券','中金公司',
    '国信证券','海通证券','民生证券','平安证券','山西证券', '上海证券', '申万宏源', '太平洋', '天风证券','信达证券', '兴业证券','中国银河', '中泰证券','艾瑞股份','财通证券','T研究','信和研究院',
    '中信建投', '中信证券', '中银国际', '中国信通院', '莫尼塔投资', '基业常青经济研究院','华创证券','方正证券','西部证券','易观国际','新时代证券','国海证券','招商证券','TokenClub 研究院',
    '中国科学院', '火币研究院', '亿欧网盟','长城证券', '中商产业研究院','恒大研究院', '麦肯锡咨询','房地产经纪人学会', '品途智库','基金业协会','红杉','链家','国联证券','联讯证券','中航证券', 
    '德勤', '鲸准研究院', '弘则弥道', '文军智库','渤海证券','财达证券','财富证券','川财证券','国都证券','国元证券','华融证券','交银国际证券','开源证券','农银国际证券','群益证券','万联证券',
    '西南证券','浙商证券','中邮证券','中原证券','爱建证券','宝通证券','财通国际','大华继显','海通国际','泓福证券','凯基证券亚洲','民信证券','摩根大通证券','瑞银证券','西证国际证券','信达国际控股',
    '耀才证券','英皇证券','越秀证券','招银国际','致富证券','中州国际证券','辉立证券','华宝证券','德意志银行','摩根士丹利']
    # test_file('E:/项目/Demo/试运行/201808',name_lists1)
    classify_file('E:/项目/试运行/SAMPLE_PDF/2018-09-20/期货期权研究',name_lists)



