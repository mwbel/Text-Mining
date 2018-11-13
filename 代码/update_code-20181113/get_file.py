import os
import shutil

def get_allfile(file_path,out_path):
    '''
    获取指定路径中所有文件(不止是PDF)
    参数:
    file_path：根目录
    out_path：输出目录
    '''
    lists = os.listdir(file_path)
    for i in lists:
        path=os.path.join(file_path,i)
        if os.path.isdir(path):
            get_allfile(path,out_path)
        else:
            if os.path.isfile(path):
                shutil.copy(path,out_path)
if __name__ == "__main__":
    get_allfile('D:/测试文件/111','D:/111')