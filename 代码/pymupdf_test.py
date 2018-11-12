import os, os.path
import shutil
import os.path
import fitz

def mkdir(path):
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
    makepath =  'D:\\项目\\test\\'
    # for root, dirnames, files in os.walk(path):
    #     print(files)
    for file in os.listdir(path):
        # print(file)

        doc = fitz.open(os.path.join(path, file))
        page_count = doc.pageCount
        doc.close()
        for key,value_list in category.items():
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

def get_contents(path):
    '''
    提取内容目录和图表目录
    :param file_list: pdf文件路径列
    :return:
    '''
    for file in os.listdir(path):
        if file[-4:] == '.pdf':
            doc=fitz.open(os.path.join(path, file))
            page_count = doc.pageCount
            # print(page_count)
            # print(doc.getToC())
            text = file
            # print(text)
            for i in range(1,page_count):
                page=doc.loadPage(i)
                # print(page)
                links = page.getLinks()
                if len(links) and links[0]['kind']==1:
                    # print(page.getText())
                    text = text + page.getText()
                    # print(links[0]['kind'])
                    # print(links)
                    # print(i)
                    # print(page.getText())
            # print(text)
            doc.close()
            pos = file.index('.')
            newname = file[:pos + 1] + 'txt'
            mkpath = path + "\\已提取"
            mkdir(mkpath)
            shutil.move(os.path.join(path, file), os.path.join(mkpath, file))
            with open(os.path.join(mkpath, newname), 'w') as file_object:
                file_object.write(text)

def deal_catalog(path):
    '''
    目录修改
    :param file_list: pdf文件路径列
    :return:
     '''
    keyword = '目录'
    keyword1 = '..'
    keyword2 = '：'
    keyword3 = '.pdf'
    for file in os.listdir(path):
        if file[-4:] =='.txt':
            # print(file_name)
            file_name1 = os.path.join(path, file)
            fro = open(file_name1, "r")
            filelist = fro.readlines()
            result = []
            for fileline in filelist:
                # print(fileline,len(fileline))
                if keyword in fileline:
                    result.append('\n')
                    result.append(fileline + '\n')
                    result.append('\n')
                if keyword1 in fileline or keyword2 in fileline or keyword3 in fileline:
                    result.append(fileline)
                else:
                    continue
            fro.close()
            count = 0
            for deal in result:
                if '图表目录' in deal and '..' not in deal:
                    break
                count += 1
            # print(count)
            list1 = result[0:count]
            # list2 = result[count:]
            list2 = []
            pos = file.index('.')
            newname = file[:pos + 1] + 'pdf'
            list2.append(newname + '\n')
            list2.append('\n')
            for i in range(count, len(result)):
                # print(result[i])
                list2.append(result[i])
            os.remove(file_name1)
            last_file_name = os.path.join(path, '目录-' + file)
            last_file_name1 = os.path.join(path, '图表目录-' + file)

            with open(last_file_name, 'w') as f:
                f.writelines(list1)

            with open(last_file_name1, 'w') as f:
                f.writelines(list2)

if __name__=='__main__':
    # rootdir = input("Enter your file path:")
    rootdir1 = ''  #'D:\\项目\\201808'
    #rootdir2 =  'D:\\项目\\demo\\已提取'
    # file_list = file_move(rootdir)
    get_contents(rootdir1)
    # deal_catalog(rootdir2)



