import fitz
import os
import shutil
import re
from broker import *
from company_classify import *

def filter_fig_rect(page,fig_rect):
    wordlist=['图','表',':','：','0','1','2','3','4','5','6','7','8','9',' ']
    new_fig_rect=[]
    words=page.getTextWords()
    for rect in fig_rect:
        # left=fitz.Rect(rect.x0-1-0.3*28,rect.y0,rect.x0-1,rect.y0+0.3*28)
        left=fitz.Rect(rect.x0-0.2*28,rect.y0+0.08*28,rect.x0-0.08*28,rect.y0+0.2*28)
        wordsleft = [w for w in words if fitz.Rect(w[:4]).intersects(left)]
        # up=fitz.Rect(rect.x0,rect.y0-1-0.3*28,rect.x0+0.3*28,rect.y0-1)
        up=fitz.Rect(rect.x0+0.08*28,rect.y0-0.2*28,rect.x0+0.2*28,rect.y0-0.08*28)
        wordsup = [w for w in words if fitz.Rect(w[:4]).intersects(up)]
        print(wordsleft,wordsup)
        # if not len(wordsup):
        if len(wordsleft):
            words_left=wordsleft[0][4]
            if len(wordsleft[0][4])>3:
                words_left=wordsleft[0][4][0:3]
                print(words_left)
            flag=0
            for word in words_left:
                if not(word in wordlist):
                    flag=1
            if flag == 0:
                new_fig_rect.append(rect)    
        else:
            new_fig_rect.append(rect)
    return new_fig_rect

def get_figrect_0(page,fignum,tablenum):
    '''
    搜索一页中所有的'图+数字'和'表+数字'矩形框
    参数:  
        page:PDF的某一页(fitz.Page)
        fignum:本页图片数起始值
        tablenum:本页表格数起始值
    返回:
        fig_rects:图片矩形框列表
        table_rects:表格矩形框列表
        fignum:下一页图片起始值
        tablenum:下一页图片起始值
    '''
    fig_rects=[]
    # table_rects=[]
    ##搜'图 1'
    fig_rect_0=page.searchFor('图 '+str(fignum))
    fig_rect_1=page.searchFor('图'+str(fignum))
    fig_rect_0.extend(fig_rect_1)
    # print(fig_rect_0,fig_rect_1,fig_rect_0)
    fig_rect=filter_fig_rect(page,fig_rect_0)
    
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('图 ',fignum,len(fig_rect))
            fig_rects.append(['图 '+str(fignum),fig_rect[0]])
            fignum+=1
            fig_rect_0=page.searchFor('图 '+str(fignum))
            fig_rect_1=page.searchFor('图'+str(fignum))
            fig_rect_0.extend(fig_rect_1)
            fig_rect=filter_fig_rect(page,fig_rect_0)
    table_rect_0=page.searchFor('表 '+str(tablenum))
    table_rect_1=page.searchFor('表'+str(tablenum))
    table_rect_0.extend(table_rect_1)
    fig_rect=filter_fig_rect(page,table_rect_0)
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('表 ',tablenum,len(table_rect))
            fig_rects.append(['表 '+str(tablenum),fig_rect[0]])
            tablenum+=1
            table_rect_0=page.searchFor('表 '+str(tablenum))
            table_rect_1=page.searchFor('表'+str(tablenum))
            table_rect_0.extend(table_rect_1)
            fig_rect=filter_fig_rect(page,table_rect_0)
    print(fig_rects)
    return fig_rects,fignum,tablenum


def get_figrect_1(page,fignum,tablenum):
    '''
    搜索一页中所有的'图表+数字'矩形框
    参数:  
        page:PDF的某一页(fitz.Page)
        fignum:本页图片数起始值
        tablenum:本页表格数起始值
    返回:
        fig_rects:图片矩形框列表
        fignum:下一页图片起始值
        tablenum:下一页图片起始值
    '''
    fig_rects=[]
    # table_rects=[]
    ##搜'图表1'
    fig_rect=page.searchFor('图表'+str(fignum))
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('图 ',fignum,len(fig_rect))
            fig_rects.append(['图表'+str(fignum),fig_rect[0]])
            fignum+=1
            fig_rect=page.searchFor('图表'+str(fignum))
    ##搜'图 表1'
    fig_rect=page.searchFor('图 表'+str(fignum))
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('图',fignum,len(fig_rect))
            fig_rects.append(['图 表'+str(fignum),fig_rect[0]])
            fignum+=1
            fig_rect=page.searchFor('图 表'+str(fignum))
    ##搜'图表 1'
    fig_rect=page.searchFor('图表 '+str(fignum))
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('图',fignum,len(fig_rect))
            fig_rects.append(['图表 '+str(fignum),fig_rect[0]])
            fignum+=1
            fig_rect=page.searchFor('图表 '+str(fignum))
    ##搜'图 表 1'
    fig_rect=page.searchFor('图 表 '+str(fignum))
    if len(fig_rect)>0:
        while len(fig_rect)>0:
            # print('图',fignum,len(fig_rect))
            fig_rects.append(['图 表 '+str(fignum),fig_rect[0]])
            fignum+=1
            fig_rect=page.searchFor('图 表 '+str(fignum))

    return fig_rects,fignum,tablenum


def get_sourcerect(page):
    '''
    搜索一页中来源所在矩形框
    参数:
        page:PDF的某一页(fit.Page)
    返回:
        sourcerects:'来源'所在矩形框的list
    '''
    sourcerects=page.searchFor('来源')
    # print(len(sourcerects))
    return sourcerects

def match_fig_source(fig_rects,sourcerect,page_length,page_width):
    '''
    匹配图表矩形框和来源矩形框
    参数:
        fig_rects:图片矩形框列表
        table_rects:表格矩形框列表
        sourcerect:来源矩形框列表
        page_length:页面长度
        page_width:页面宽度
    返回:
        match:匹配成功后的图表来源矩形框列表
        rest_name_figrect:跨页的图表矩形框
    '''
    match=[]
    rest_name_figrect=[]
    for fig_rect in fig_rects:
        fig_source=fitz.Rect(page_length,page_width,page_length,page_width)
        for source in sourcerect:
            
            if source.y0-fig_rect[1].y0>0.9*28:
                if fig_rect[1].tl.distance_to(source.tl)<fig_rect[1].tl.distance_to(fig_source):
                    fig_source=source
        if fig_source == fitz.Rect(page_length,page_width,page_length,page_width):
            rest_name_figrect.append(fig_rect)
        else:
            match.append([fig_rect[0],fig_rect[1],fig_source])
    return match,rest_name_figrect

def group_name_figrect_sourcerects(name_figrect_sourcerects):
    '''
    将图片按行分组
    '''
    # print(name_figrect_sourcerects)
    name_figrect_sourcerects=sorted(name_figrect_sourcerects,key=take_y0_x0)
    # print('---------------------')
    # for name_figrect_sourcerect in name_figrect_sourcerects:
    #     print(name_figrect_sourcerect[0],name_figrect_sourcerect[1],name_figrect_sourcerect[2])
    # print(name_figrect_sourcerects)
    name_figrect_sourcerect_row=[[]]
    length = len(name_figrect_sourcerects)  # 图表数
    for i in range(length):  # 将图表按行分组
        if i < (length - 1):
            if abs(name_figrect_sourcerects[i][1].y0-name_figrect_sourcerects[i+1][1].y0)<8:
                # print(abs(name_figrect_sourcerects[i][1].y0-name_figrect_sourcerects[i+1][1].y0))
                name_figrect_sourcerect_row[-1].append(name_figrect_sourcerects[i])
            else:
                name_figrect_sourcerect_row[-1].append(name_figrect_sourcerects[i])
                name_figrect_sourcerect_row.append([])
    name_figrect_sourcerect_row[-1].append(name_figrect_sourcerects[i])
    name_figrect_sourcerect_row1=[]
    for row in name_figrect_sourcerect_row:
        name_figrect_sourcerect_row1.append(sorted(row,key=take_x0))

    # print(name_figrect_sourcerect_row)
    # print(name_figrect_sourcerect_row1)
    return name_figrect_sourcerect_row1

def take_x0(elem):
    '''
    提取矩形框的x0坐标
    参数:
        elem:
    '''
    # print(elem)
    return elem[1].x0

def take_y0_x0(elem):
    '''
    提取矩形框的y0,x0坐标
    参数:
        elem:
    '''
    # print(elem)
    return elem[1].y0,elem[1].x0

def extra_rest_fig(page,page1,source_rects_1,rest_name_figrect,page_length,page_width,out_path,broker_arg):
    '''
    提取拼接跨页图片后保存
    0：图表分开命名0 图表统一命名1
    1：图表名位置 靠左0 居中1 靠右2
    2：来源位置 靠左0 居中1 靠右2
    3：页边距(右侧)
    4：页边距(下侧)
    5：页边距(上侧)
    6：图表左侧坐标偏移(分情况) 
    7：一行多个图片时图片间的间距(分情况) 
    8：图表名字号高度
    '''
    mat = fitz.Matrix(3, 3)
    rest_name_figrect=sorted(rest_name_figrect,key=take_x0)
    if len(rest_name_figrect)>len(source_rects_1):
        for i in range(len(rest_name_figrect)-len(source_rects_1)):
            source_rects_1.append(fitz.Rect(0,0,page_length-broker_arg[3]*28,page_width-broker_arg[4]*28))      
    for i in range(len(rest_name_figrect)):
        if i < len(rest_name_figrect) - 1:
            if broker_arg[1]==0:
                rect1=fitz.Rect(rest_name_figrect[i][1].x0 - broker_arg[6]*28, rest_name_figrect[i][1].y0, rest_name_figrect[i+1][1].x0 - broker_arg[7]*28,page_width-broker_arg[4]*28)
                rect2=fitz.Rect(rest_name_figrect[i][1].x0 - broker_arg[6]*28,broker_arg[5]*28, rest_name_figrect[i+1][1].x0 - broker_arg[7]*28,source_rects_1[i].y1)
            else:
                rect1=fitz.Rect(source_rects_1[i].x0 - broker_arg[6]*28, rest_name_figrect[i][1].y0, source_rects_1[i+1].x0 - broker_arg[7]*28,page_width-broker_arg[4]*28)
                rect2=fitz.Rect(source_rects_1[i].x0 - broker_arg[6]*28,broker_arg[5]*28, source_rects_1[i+1].x0 - broker_arg[7]*28,source_rects_1[i].y1)
            pix = page.getPixmap(matrix=mat, clip=rect1, alpha=False)
            pix1 = page1.getPixmap(matrix=mat, clip=rect2, alpha=False)
            tar_irect  = fitz.IRect(0, 0, pix.width,pix.height+pix1.height)
            tar_pix  = fitz.Pixmap(fitz.csRGB, tar_irect, pix.alpha)
            tar_pix.clearWith(90)
            pix.x=0
            pix.y=0
            pix1.x=0
            pix1.y=pix.height
            tar_pix.copyPixmap(pix,pix.irect)
            tar_pix.copyPixmap(pix1,pix1.irect)
            rect1.y1=rect1.y0+broker_arg[8]*28
            figname=get_figname(page,rect1)
            figname=validateTitle(figname)
            fig_name = figname + ".png" 
            tar_pix.writePNG(os.path.join(out_path, fig_name))
        else:
            if broker_arg[1]==0:
                rect1=fitz.Rect(rest_name_figrect[i][1].x0 - broker_arg[6]*28, rest_name_figrect[i][1].y0,page_length - broker_arg[3]*28,page_width-broker_arg[4]*28)
                rect2=fitz.Rect(rest_name_figrect[i][1].x0 - broker_arg[6]*28,broker_arg[5]*28, page_length - broker_arg[3]*28,source_rects_1[i].y1)
            else:
                rect1=fitz.Rect(source_rects_1[i].x0 - broker_arg[6]*28, rest_name_figrect[i][1].y0,page_length - broker_arg[3]*28,page_width-broker_arg[4]*28)
                rect2=fitz.Rect(source_rects_1[i].x0 - broker_arg[6]*28,broker_arg[5]*28,page_length - broker_arg[3]*28,source_rects_1[i].y1)
            pix = page.getPixmap(matrix=mat, clip=rect1, alpha=False)
            pix1 = page1.getPixmap(matrix=mat, clip=rect2, alpha=False)
            tar_irect  = fitz.IRect(0, 0, pix.width,pix.height+pix1.height)
            tar_pix  = fitz.Pixmap(fitz.csRGB, tar_irect, pix.alpha)
            tar_pix.clearWith(90)
            pix.x=0
            pix.y=0
            pix1.x=0
            pix1.y=pix.height
            tar_pix.copyPixmap(pix,pix.irect)
            tar_pix.copyPixmap(pix1,pix1.irect)
            rect1.y1=rect1.y0+broker_arg[8]*28
            figname=get_figname(page,rect1)
            figname=validateTitle(figname)
            fig_name = figname + ".png" 
            tar_pix.writePNG(os.path.join(out_path, fig_name))

def make_rect(name_figrect_sourcerect_row,page_length,page_width,broker_arg):
    '''
    根据图表矩形框和来源矩形框构造矩形框

    0：图表分开命名0 图表统一命名1
    1：图表名位置 靠左0 居中1 靠右2
    2：来源位置 靠左0 居中1 靠右2
    3：页边距(右侧)
    4：页边距(下侧)
    5：页边距(上侧)
    6：图表左侧坐标偏移(分情况) 
    7：一行多个图片时图片间的间距(分情况) 
    8：图表名字号高度
    '''
    name_rects=[]
    for row in name_figrect_sourcerect_row:
        for i in range(len(row)):
            if i < len(row) - 1:
                if broker_arg[1]==0:
                    clip = fitz.Rect(row[i][1].x0 - broker_arg[6]*28, row[i][1].y0, row[i+1][1].x0 - broker_arg[7]*28,row[i][2].y1)
                else:
                    clip = fitz.Rect(row[i][2].x0 - broker_arg[6]*28, row[i][1].y0, row[i+1][2].x0 - broker_arg[7]*28,row[i][2].y1)
                name_rects.append([row[i][0],clip])
            else:
                if broker_arg[1]==0:
                    clip = fitz.Rect(row[i][1].x0 - broker_arg[6]*28, row[i][1].y0, page_length - broker_arg[3]*28,row[i][2].y1)
                else:
                    clip = fitz.Rect(row[i][2].x0 - broker_arg[6]*28, row[i][1].y0, page_length - broker_arg[3]*28,row[i][2].y1)
                name_rects.append([row[i][0],clip])
    # print(name_rects)
    return name_rects

def get_figname(page,fig_rect):
    '''
    根据图表名所在矩形框获取图表的名字
    只要文字的一部分在矩形框中就可以提取
    参数:
        page:图表所在页(fitz.Page)
        fig_rect:图表名所在矩形框(fitz.Rect)
    返回:
        figname:图表名
    '''
    # print('-------------------------')
    words = page.getTextWords()
    # mywords = [w for w in words if fitz.Rect(w[:4]) in fig_rect]
    mywords = [w for w in words if fitz.Rect(w[:4]).intersects(fig_rect)]
    figname=' '
    for i in range(len(mywords)):
        flag=-1
        if i < len(mywords)-1:
            for j in range(min(len(mywords[i][4]),len(mywords[i+1][4]))):
                if mywords[i][4][-1-j:] == mywords[i+1][4][0:j+1]:
                    # print(mywords[i][4][-1-j:],mywords[i+1][4][0:j+1])
                    flag=j
            if flag == -1:
                figname+=' '+mywords[i][4]
            else:
                figname+=' '+mywords[i][4][0:-1-flag]
        else:
            figname+=' '+mywords[i][4]
    if not figname[0]=='图' or figname[0] == '表':
        for k in range(len(figname)):
            if figname[k]=='图':
                figname=figname[k:]
                break
            if figname[k]=='表':
                figname=figname[k:]
                break
    print(figname)
    # for a in mywords:
    #     print(a[4])
    return figname

def validateTitle(title):
    '''
    将图表名中非法字符替换为下划线(_)
    参数:
        title:原图表名
    返回:
        new_title:替换后的图表名
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def extract_fig(page,name_rects,out_path,broker_arg):
    '''
    根据name_rects提取图片并保存
    参数:
        page:图片所在页(fitz.Page)
        name_rects:图片的rect(fitz.Rect)
        out_path:输出路径
    '''
    mat = fitz.Matrix(3, 3)#图片缩放
    for name_rect in name_rects:
        pix = page.getPixmap(matrix=mat, clip=name_rect[1], alpha=False)
        name_rect[1].y0=name_rect[1].y0+5
        name_rect[1].y1=name_rect[1].y0+broker_arg[8]*28
        # pix2 = page.getPixmap(matrix=mat, clip=name_rect[1], alpha=False)
        figname=get_figname(page,name_rect[1])
        figname=validateTitle(figname)
        fig_name = figname + ".png"  
        # fig_name2 = name_rect[0] + "Ming.png"
        pix.writePNG(os.path.join(out_path, fig_name))
        # pix2.writePNG(os.path.join(out_path, fig_name2))
        # print(name_rect[0],name_rect[1])



# if __name__ == "__main__":
#     path = "E:/项目/Demo/试运行-2/试运行/201808/按券商分类"
#     broker_lists = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))]
#     for broker_list in broker_lists:
#         file_path=os.path.join(path,broker_list)
#         out_path=os.path.join("E:/pic/2",broker_list)
#         failure_path = "E:/pic/2/未处理完成"
#         if not os.path.exists(failure_path):
#             os.makedirs(failure_path)
#         pdf_files = [name for name in os.listdir(file_path) if name.endswith('.pdf')]
#         for pdf in pdf_files:
#             try:
#                 pdf_path=os.path.join(file_path,pdf)
#                 ##TODO根据名字确定券商
#                 broker_arg=get_brokerarg(broker_list)
#                 out_path=os.path.join("E:/pic/2",broker_list)
#                 out_path=os.path.join(out_path,os.path.splitext(os.path.basename(pdf_path))[0])
#                 if not os.path.exists(out_path):
#                     os.makedirs(out_path)
#                 shutil.copy(pdf_path,out_path)
#                 print(pdf)
#                 pdf_path=os.path.join(file_path,pdf)
                
#                 if broker_arg:
#                     doc=fitz.open(pdf_path)
#                     pagenum=doc.pageCount
#                     fignum=1
#                     tablenum=1
#                     for i in range(pagenum):
#                         page=doc.loadPage(i)
#                         text=page.getText()
#                         if not '.......' in text:
#                             page_ = page.rect  # 页面大小
#                             page_length = page_.x1  # 页面长
#                             page_width = page_.y1  # 页面宽
#                             sourcerect=get_sourcerect(page) #搜索来源rect
#                             if i+1 > pagenum-1: #搜索跨页来源rect
#                                 source_rects_1=[]
#                             else:
#                                 page1=doc.loadPage(i+1)
#                                 source_rects_1=get_sourcerect(page1)
#                             # print(i+1,'页')
#                             #搜索图表rect
#                             if broker_arg[0]==0:
#                                 fig_rects,fignum,tablenum=get_figrect_0(page,fignum,tablenum)
#                             else:
#                                 fig_rects,fignum,tablenum=get_figrect_1(page,fignum,tablenum)
#                             #匹配 图表rect和来源rect
#                             name_figrect_sourcerects,rest_name_figrect=match_fig_source(fig_rects,sourcerect,page_length,page_width)
#                             #分别处理跨页图表和非跨页图表
#                             if len(rest_name_figrect):#跨页
#                                 extra_rest_fig(page,page1,source_rects_1,rest_name_figrect,page_length,page_width,out_path,broker_arg)
#                             if len(name_figrect_sourcerects):#不跨页
#                                 name_figrect_sourcerect_row=group_name_figrect_sourcerects(name_figrect_sourcerects)
#                                 name_rects=make_rect(name_figrect_sourcerect_row,page_length,page_width,broker_arg)
#                                 extract_fig(page,name_rects,out_path,broker_arg)
#                     doc.close()
#                     print(out_path)
#                     pdf_and_fig_lists = os.listdir(out_path)
#                     print(len(pdf_and_fig_lists))
#                     if os.path.isdir(out_path) and len(pdf_and_fig_lists) <= 4 :
#                         if not os.path.exists(os.path.join(failure_path,os.path.splitext(os.path.basename(pdf_path))[0])):
#                             shutil.move(out_path,failure_path)
#                 else:
#                     if not os.path.exists(os.path.join(failure_path,os.path.splitext(os.path.basename(pdf_path))[0])):
#                         shutil.move(out_path,failure_path)         
#             except:
#                 print(out_path)
#                 if not os.path.exists(os.path.join(failure_path,os.path.splitext(os.path.basename(pdf_path))[0])):
#                     shutil.move(out_path,failure_path)
#                 continue


if __name__ == "__main__":
    #file_path="E:/pic/测试/中国科学院"
    file_path="/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/未处理的报告"
    # file_path="D:/test"
    out_path="/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/未处理的报告"
    pdf_files = [name for name in os.listdir(file_path) if name.endswith('.pdf')]
    for pdf in pdf_files:
        pdf_path=os.path.join(file_path,pdf)
        ##TODO根据名字确定券商
        broker_arg=get_brokerarg('中国科学院')
        print(broker_arg)
        if broker_arg:
            #out_path="E:/pic/3/中国科学院/"
            out_path="/Users/Pro/Documents/Others/应用项目/Text Mining/待处理/201808/未处理的报告"
            out_path=os.path.join(out_path,os.path.splitext(os.path.basename(pdf_path))[0])
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            shutil.copy(pdf_path,out_path)
            print(pdf)
            pdf_path=os.path.join(file_path,pdf)
            doc=fitz.open(pdf_path)
            pagenum=doc.pageCount
            fignum=1
            tablenum=1
            for i in range(1,pagenum):
                page=doc.loadPage(i)
                text=page.getText()
                point_count = text.count(".")
                print("点的个数：",point_count)
                if point_count<=80:
                    page_ = page.rect  # 页面大小
                    page_length = page_.x1  # 页面长
                    page_width = page_.y1  # 页面宽
                    sourcerect=get_sourcerect(page) #搜索来源rect
                    if i+1 > pagenum-1: #搜索跨页来源rect
                        source_rects_1=[]
                    else:
                        page1=doc.loadPage(i+1)
                        source_rects_1=get_sourcerect(page1)
                    print(i+1,'页')
                    #搜索图表rect
                    if broker_arg[0]==0:
                        fig_rects,fignum,tablenum=get_figrect_0(page,fignum,tablenum)
                    else:
                        fig_rects,fignum,tablenum=get_figrect_1(page,fignum,tablenum)
                    #匹配 图表rect和来源rect
                    name_figrect_sourcerects,rest_name_figrect=match_fig_source(fig_rects,sourcerect,page_length,page_width)
                    #分别处理跨页图表和非跨页图表
                    if len(rest_name_figrect):#跨页
                        extra_rest_fig(page,page1,source_rects_1,rest_name_figrect,page_length,page_width,out_path,broker_arg)
                    if len(name_figrect_sourcerects):#不跨页
                        name_figrect_sourcerect_row=group_name_figrect_sourcerects(name_figrect_sourcerects)
                        name_rects=make_rect(name_figrect_sourcerect_row,page_length,page_width,broker_arg)
                        extract_fig(page,name_rects,out_path,broker_arg)
            doc.close()




