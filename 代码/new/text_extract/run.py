from image_extract import *
from catalog_grouping import *
from source_classify import *
import fitz
import operator
import re
import os
import shutil

if __name__ == "__main__":
    file_path="E:/项目/试运行/201808/需求4/处理完成"
    out_path="E:/项目/试运行/201808/需求4/处理完成/提取图片"
  
    # file_path="E:/项目/试运行/201808/需求4/处理完成/测试/测试/资料来源"
    # out_path="E:/项目/试运行/201808/需求4/处理完成/测试/测试/提取图片"
    
    # file_path="E:/项目/试运行/201808/需求4/处理完成/测试/测试/来源"
    # out_path="E:/项目/试运行/201808/需求4/处理完成/测试/测试/提取图片"
    pdf_files = [name for name in os.listdir(file_path) if name.endswith('.pdf')]
    fail_path=os.path.join(out_path,'未处理完成')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if not os.path.exists(fail_path):
        os.makedirs(fail_path)
    for pdf in pdf_files:
        try:
            pdf_path=os.path.join(file_path,pdf)
            source = preprocess(file_path,pdf)
            if source == "来源": 
                file_type=0
            elif source == "资料来源":
                file_type=1
            elif source == "数据来源":
                file_type=2
            elif source == "未处理完成":
                file_type=-1
                shutil.copy(pdf_path,os.path.join(fail_path,pdf))
            name_list,first_page,flag = catalog_extract(pdf_path)
            # print(name_list)
            # print(pdf)
            if not(file_type == -1):
                if not len(name_list): 
                    shutil.copy(pdf_path,os.path.join(fail_path,pdf))
                else:
                    fig_name = catalog_list_grouping(name_list)
                    image_extract(pdf_path,out_path,fig_name,file_type,first_page,flag)
        except :
            print(pdf)
            continue

        