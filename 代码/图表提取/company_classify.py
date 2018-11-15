import fitz
import os
import shutil


# def classify_file(path, name_file):
#     # if not os.path.exists(os.path.join(path,'represents')):
#     #     os.makedirs(os.path.join(path,'represents'))
#     with open(name_file, 'r', encoding = 'utf-8') as file:
#         name_lists1 = file.readlines()
#     print(name_lists1)
#     name_lists = []
#     for name_list1 in name_lists1:
#         if len(name_list1.strip('\n')):
#             name_lists.append(name_list1.strip('\n'))
#     print(name_lists)
#     for name in os.listdir(path):
#         if name.endswith('.pdf'):
#             for name_list in name_lists:
#                 output_path = os.path.join(path, name_list)
#                 if not os.path.exists(output_path):
#                     os.makedirs(output_path)
#                 if name_list in name:.
#                     shutil.copy(os.path.join(path,name), output_path)

# 挑出页数大于10页的pdf文件
def max_page(path):
    failure_path = os.path.join(path,"未处理完成")
    if not os.path.exists(failure_path):
        os.makedirs(failure_path)
    for file in os.listdir(path):
        if not file.endswith(".pdf"):
            if not os.path.exists(os.path.join(failure_path,file)):
                shutil.move(os.path.join(path,file),failure_path)
    pdf_files = [name for name in os.listdir(path) if name.endswith(".pdf")]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(path,pdf_file)
        doc = fitz.open(pdf_path)
        pagenum = doc.pageCount
        doc.close()
        print(pdf_file,pagenum)
        if pagenum<=10:
            if not os.path.exists(os.path.join(failure_path,pdf_file)):
                shutil.move(pdf_path,failure_path)
            continue       

# 按照券商名称分类
def classify_file(path, name_file):
    '''
    # 输入：path: pdf文件路径
         # name_file: 券商名称文件
    # 输出：按照券商名称分类好的文件夹
    '''
    # if not os.path.exists(os.path.join(path,'represents')):
    #     os.makedirs(os.path.join(path,'represents'))
    with open(name_file, 'r', encoding = 'utf-8') as file:
        name_lists1 = file.readlines()
    # print(name_lists1)
    name_lists = []
    out_namelists = []
    for name_list1 in name_lists1:
        if len(name_list1.strip('\n')):
            name_lists.append(name_list1.strip('\n'))
    name_lists = list(set(name_lists))
    # print(name_lists)
    pdf_files = [name for name in os.listdir(path) if name.endswith(".pdf")]
    for name in pdf_files:
        title_name = name.split('-')
        print(title_name)
        for name_list in name_lists:
            output_path =os.path.join(os.path.join(path,'按券商分类'), name_list)
            if len(title_name)==1 and name_list in title_name[0]:
                if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    # shutil.copy(os.path.join(path, name), output_path)
                if not os.path.exists(os.path.join(output_path, name)):
                    shutil.move(os.path.join(path, name), output_path)
                    # shutil.copy(os.path.join(path, name), output_path)
                out_namelists.append(name_list)
            else:
                for i in range(len(title_name)):
                    if name_list == title_name[i]:
                        if not os.path.exists(output_path):
                            os.makedirs(output_path)
                        # shutil.copy(os.path.join(path, name), output_path)
                        if not os.path.exists(os.path.join(output_path, name)):
                            shutil.move(os.path.join(path, name), output_path)
                            # shutil.copy(os.path.join(path, name), output_path)
                        out_namelists.append(name_list)
                        break     
    return os.path.join(path,'按券商分类')

if __name__=='__main__':
    # classify_extract('E:/20180801-广证恒生-【新型制剂系列专题】ALZA：载药技术先驱的崛起与启示.pdf')
    # name_lists = ['民生', '太平洋', '国金', '华创', '申万宏源', '兴业', '中信', '方正', '中银国际', '安信', '广发', '平安','中泰','光大','华泰','国泰君安','海通','国信','财通','东方','东兴','招商','莫尼塔','东北','新时代','','','','','']
    # name_lists = ['爱建证券', '安信证券', '北京高华证券', '渤海证券', '渤海汇金证券', '财达证券', '财富证券', '财通证券', '长城国瑞证券', '长城证券', '长江证券', '川财证券', '大通证券',
    #  '大同证券', '德邦证券', '第一创业证券', '东北证券', '东方花旗证券', '东方证券', '东海证券', '东莞证券', '东吴证券', '东兴证券', '东亚前海证券', '东证融汇证券', '方正证券',
    #  '高盛高华证券', '光大证券', '广发证券', '广证恒生', '广州证券', '国都证券', '国海证券', '国金证券', '国开证券', '国联证券', '国融证券', '国盛证券', '国泰君安证券', '国信证券',
    #  '国元证券', '海通证券', '恒泰长财证券', '恒泰证券', '红塔证券', '宏信证券', '华安证券', '华宝证券', '华创证券', '华福证券', '华金证券', '华菁证券', '华林证券', '华龙证券',
    #  '华融证券', '华泰联合证券', '华泰证券', '华西证券', '华鑫证券', '华英证券', '汇丰前海证券', '江海证券', '金通证券', '金元证券', '九州证券', '开源证券', '联储证券', '联讯证券',
    #  '民生证券', '摩根士丹利华鑫证券', '南京证券', '平安证券', '瑞信方正证券', '瑞银证券', '山西证券', '上海证券', '申万宏源证券', '申港证券', '世纪证券', '首创证券', '太平洋证券',
    #  '天风证券', '万和证券', '万联证券', '网信证券', '五矿证券', '西部证券', '西藏东方财富证券', '西南证券', '湘财证券', '新时代证券', '信达证券', '兴业证券', '兴证证券',
    #  '银河金汇证券', '银泰证券', '英大证券', '招商证券', '招商证券', '浙商证券', '中德证券', '中国国际金融', '中国民族证券', '中国银河证券', '中国中投证券', '中航证券', '中山证券',
    #  '中泰证券', '中天证券', '中天国富证券', '中信建投证券', '中信证券', '中银国际证券', '中邮证券', '中原证券', '中国信息通信研究院', '莫尼塔投资', '恒大研究院', '基业常青经济研究院',
    #  '中国科学院', '火币研究院', '亿欧网盟']
    # path = r"E:/项目/Demo/试运行-2/SAMPLE_PDF/2018-09-20"
    # broker_names = r'E:/项目/newRequest/券商名称'
    # dirs = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))]
    # for dir in dirs:
    #     if os.path.isdir(os.path.join(path,dir)): 
    #         input_path = os.path.join(path,dir)
    #         max_page(input_path)
    # for dir in dirs:
    #     input_path = os.path.join(path,dir)
    #     classify_file(input_path,os.path.join(input_path,broker_names))
    classify_file(r'D:/201808', r'D:/update_code/券商名称')