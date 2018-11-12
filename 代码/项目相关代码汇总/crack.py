# TODO: 为方便测试没有删除原文件
import fitz
import re
import sys
import io
import os
from operator import itemgetter 
from itertools import groupby
import shutil

def crack(file_path, out_path):
    """破解并移除"报告吧"水印
    对于可以破解的文件破解并移除水印，处理后存放在file_path下处理完成文件夹
    对于不可破解的文件(如:用户密码)，将文件移动到file_path下未处理完成文件夹
    
    解决破解后的PDF链接有黑色方框
    将pymupdf框架源文件utils.py中do_links的annot_goto改为
    annot_goto ='''<</F 4/BS<</W 0>>/Dest[%i 0 R /XYZ %g %g 0]/Rect[%s]/Subtype/Link>>'''

    Args:
        file_path:输入文件目录
        out_path:输出文件目录
    """
    out_path = os.path.join(file_path, "处理完成")
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    pdf_files = [name for name in os.listdir(file_path) if name.endswith('.pdf')]
    for pdf in pdf_files:
        print(pdf)
        pdf_path=os.path.join(file_path,pdf)
        fail_path=os.path.join(file_path, '未处理完成', pdf)
        out=os.path.join(out_path, pdf)
        try:
            # "报告吧"水印一般为第一个obj
            doc=fitz.open(pdf_path)
            watermark='<</Matrix[1 0 0 1 0 0]/Subtype/Form/Filter/FlateDecode/Length 261/Resources<</ExtGState<</GS0 2 0 R/GS1 3 0 R>>/XObject<</Fm1 4 0 R/Fm0 5 0 R/Fm3 6 0 R/Fm2 7 0 R>>>>/FormType 1/Type/XObject/BBox[0 0 612 792]>>'
            if doc._getObjectString(1)==watermark:
                doc._updateStream(1,b"")
                doc2=fitz.open()
                doc2.insertPDF(doc)
                doc2.save(out)
                doc2.close()
            else:
                shutil.copyfile(pdf_path, out)
            doc.close()
        except:
            print('解密失败')
            if not os.path.exists(os.path.join(file_path, '未处理完成')):
                os.makedirs(os.path.join(file_path, '未处理完成'))
            shutil.copyfile(pdf_path, fail_path)
            continue



if __name__ == '__main__':
    list = ['晨会纪要','动态点评','港股市场研究','公司分析','行业日报','行业事件点评','行业月报','基金投资策略','理财产品研究','美股公司研究','期货期权研究','其他公告点评','其他行业策略','其他投资策略','全球策略','','','','','','','','','','']
    file_path="D:/Project/project/Process/SAMPLE_PDF/2018-09-20/行业月报"
    out_path="D:/Project/Crack/"
    crack(file_path, out_path)
    print()
