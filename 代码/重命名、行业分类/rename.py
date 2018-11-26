import os, os.path
import shutil
import os.path
import fitz
import re

def rename(path):
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
        
    pdf_files = [name for name in os.listdir(path) if name.endswith('.pdf')]
    for file in pdf_files:
        # print(file)
        doc = fitz.open(os.path.join(path, file))
        page_count = doc.pageCount
        doc.close()
        pagekey = str(page_count) + '页'
        for key, value_list in category.items():
            for value in value_list:
                # print(value)
                if pagekey not in file and key not in file and value in file:
                    # 重命名文件
                    if os.path.isfile(os.path.join(path, file))==True:
                        # 字符串指定位置插入字符串
                        pos1 = file.index('-')
                        pos2 = file.index('.')
                        # 新名称：加上行业大分类和页码
                        newname = file[:pos1+1] + key+'-' + file[pos1+1:pos2] + '-' + pagekey + file[pos2:]
                        # print(newname)
                        os.rename(os.path.join(path, file), os.path.join(path, newname))
                    break
        continue

if __name__ == '__main__':
    path = r"E://项目//测试//测试//试运行//201808"
    rename(path)