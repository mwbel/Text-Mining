import os, os.path
import shutil
import os.path
import fitz
import re


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

def file_move(path):
    '''
    给文件重命名并移动到指定位置
    :param file_list: 文件列表
    :return:
    '''
    category = {
        '大消费': ['旅游', '电商', '教育', '跨境', '母婴',
                '物流', '快递', '连锁', '家居', '美容',
                '网红', '时尚', '化妆品', '学校', '农药',
                '零售', '生鲜', '啤酒', '果汁', '乳业',
                '宠物', '出行', '早教', '餐饮', '培训','黄金'],
        '生命健康': ['新药', '医疗器械', '基因', 'CRO',
                 '医院', '肿瘤', 'IVD', 'POCT', '糖尿病',
                 '疫苗', '血制品', '保健', '麻醉', '体检',
                 '康复', 'CMO', 'HPV', '医疗美容', '免疫',
                 '药店', '心血管', '透析', '影像', '维生素',
                 '中药','制剂'],
        '先进制造': ['半导体', '无人机', '高铁', '汽车',
                 '材料', '工业4.0', '机器人', 'LED', '硬件',
                 '航空', '手机', '摄像头', '装备',
                 'PCB', '航天', '卫星', '硅片'],
        '传媒娱乐': ['直播', '体育', '电影', '游戏', '音乐',
                 '广告', '动漫', '文学', '视频', '社交',
                 '彩票', '足球', '社区', '音频', '女性',
                 '博彩', '电竞', '阅读', '知识付费'],
        '信息科技': ['大数据', 'O2O', '软件', 'SAAS', '安全',
                 '物联网', '人工智能', '5G', 'AR', 'VR',
                 '共享', '3D', '无人驾驶', '智能硬件', '区块链',
                 '信息化', '工业控制', '通讯', '互联网',
                 '量子', '北斗', '通信'],
        '节能环保': ['电池', '光伏', '大气', '风电', '水处理',
                 '储能', '新能源', '碳排放', '核电', '环卫',
                 '危废', '再生', '环保'],
        '地产金融': ['互联网金融', '征信', '物流地产', 'P2P',
                 '消费金融', '支付', '房地产', '银行', '保险',
                 '证券', '比特币', '养老', '公寓', '金融科技',
                 'REITs', '资管', '租赁', '供应链金融',
                 '汽车金融', '财富', '不良资产', '物业'],
        '其它产业': ['电力', '军工', '大农业', '化工', '纺织',
                 '建筑', '家电', '石油', '有色金属']
    }
    makepath = 'D:\\项目\\试运行\\test\\'
    # for root, dirnames, files in os.walk(path):
    #     print(files)
    for file in os.listdir(path):
        # print(file)
        doc = fitz.open(os.path.join(path, file))
        page_count = doc.pageCount
        doc.close()
        for key, value_list in category.items():
            # print(value_list)
            # 定义要创建的目录
            mkpath = makepath + key
            # 调用创建目录的函数
            mkdir(mkpath)
            for value in value_list:
                # print(value)
                if key not in file and value in file:
                    # 重命名文件
                    if os.path.isfile(os.path.join(path, file))==True:
                        # 字符串指定位置插入字符串
                        pos1 = file.index('-')
                        pos2 = file.index('.')
                        newname = file[:pos1+1] + key+'-' + file[pos1+1:pos2] + '-' + str(page_count) + '页' + file[pos2:]
                        # print(newname)
                        os.rename(os.path.join(path, file), os.path.join(path, newname))
                        shutil.copy(os.path.join(path, newname), os.path.join(mkpath, newname))
                    break
        continue


# file_move('E:/项目/需求示例包/0000---未分类PDF文件')
def classify(path):
    '''
    将有目录和没有目录的pdf文件放到不同文件路径下
    :param path: pdf文件路径
    :return:
    '''
    keywords = '.........'
    mkpath1 = path + '\\有目录\\'
    mkdir(mkpath1)
    mkpath2 = path + '\\无目录\\'
    mkdir(mkpath2)
    for file in os.listdir(path):
        if file[-4:] == '.pdf':
            flag = False
            doc = fitz.open(os.path.join(path, file))
            for i in range(1, 10):
                page = doc.loadPage(i)
                page_text = page.getText()
                if keywords in page_text:
                    flag = True
                    break
            doc.close()
            if flag:
                shutil.move(os.path.join(path, file), os.path.join(mkpath1, file))
            else:
                shutil.move(os.path.join(path, file), os.path.join(mkpath2, file))
    return mkpath1

def get_contents(path):
    '''
    提取内容目录和图表目录
    :param file_list: pdf文件路径
    :return:
    '''
    keywords = "........"                       #判断有没有目录的处理条件
    for file in os.listdir(path):
        if file[-4:] == '.pdf':
            doc = fitz.open(os.path.join(path, file))
            # page_count = doc.pageCount
            # print(page_count)
            # print(page_count)
            # print(doc.getToC())
            text = file + '\n'                          #给提取的目录加上文件名称
            # print(text)
            for i in range(1, 10):
                page = doc.loadPage(i)
                # print(page)
                # links=page.getLinks()
                page_text = page.getText()
                # if len(links) and links[0]['kind']==1:
                    # print(page.getText())
                    # text = text + page.getText()
                    # print(links[0]['kind'])
                    # print(links)
                    # print(i)
                    # print(page.getText())
                if keywords in page_text:
                    text = text + page.getText()
            # print(text)
            doc.close()
            # print(text)
            text = text.encode("GBK", "ignore")
            pos = file.index('.')
            newname = file[:pos + 1] + 'txt'
            # print(newname)
            with open(os.path.join(path, newname), 'wb+') as file_object:
                file_object.write(text)

def deal_catalog(path):
    '''
    将提取的目录进行处理，把内容目录和图表目录分开
    :param file_list: pdf文件路径列
    :return:
     '''
    keyword = r'.*\s*目\s*录\s*'
    keyword1 = '.....'
    keyword2 = '： '
    keyword3 = '、'
    keyword4 = r'\s*图\s*表\s*'
    keyword5 = r'\d*\.\d*'
    keyword6 = r'\s*图\s*目\s*|\s*插\s*图\s*|\s*表\s*目\s*|\s*表\s*格\s*'

    for file in os.listdir(path):
        if file[-4:] == '.txt':
            # print(file_name)
            file_name1 = os.path.join(path, file)
            fro = open(file_name1, "r")
            filelist = fro.readlines()
            result = []
            for fileline in filelist:
                # print(fileline,len(fileline))
                #print(re.match(keyword, fileline, re.I))
                if (re.match(keyword, fileline, re.I) or re.match(keyword4, fileline, re.I))and '..' not in fileline:
                    result.append('\n')
                    result.append(fileline + '\n')
                    result.append('\n')
                if keyword1 in fileline or keyword2 in fileline or keyword3 in fileline or re.match(keyword5, fileline, re.I):
                    result.append(fileline)
                else:
                    continue
            fro.close()
            count = 0
            for deal in result:
                if (re.match(keyword4, deal, re.I) or re.match(keyword6, deal, re.I)) and '..' not in deal:
                    break
                count += 1
            # print(count)
            pos = file.index('.')
            newname = file[:pos + 1] + 'pdf'+'\n'
            list1 = [newname]+result[0:count]
            list2 = result[count:]
            List_2_end = []
            if len(list2) != 0:
                list_head = []
                list_head.append(newname + '\n')
                list_head.append('\n')
                List_2_end = list_head + list2

            os.remove(file_name1)              #删除原目录
            last_file_name = os.path.join(path, '目录-' + file)
            last_file_name1 = os.path.join(path, '图表目录-' + file)

            with open(last_file_name, 'w') as f:
                f.writelines(list1)
            if len(List_2_end) != 0:
                with open(last_file_name1, 'w') as f:
                    f.writelines(List_2_end)


if __name__ == '__main__':
    rootdir = input("Enter your file path:")
    deal_dir = classify(rootdir)
    # get_contents(rootdir)
    # deal_catalog(rootdir)
    get_contents(deal_dir)
    deal_catalog(deal_dir)



