import os

def fail_statistic(file_path):
    '''
    失败文件统计
    参数：
    file_path:failure_path路径
    '''
    lists = os.listdir(file_path)
    print('失败文件统计')
    fail_num=0
    for i in lists:
        path=os.path.join(file_path,i)
        broker_list=os.listdir(path)
        file_num=0
        for j in broker_list:
            file_num=file_num+len(os.listdir(os.path.join(path,j)))
        fail_num=fail_num+file_num
        print(i,file_num)
    print('共',fail_num,'个文件')


def success_statistic(file_path):
    '''
    成功文件统计
    参数：
    file_path：已处理完成路径
    '''
    lists = os.listdir(file_path)
    print('成功文件统计')
    success_num=0
    for i in lists:
        path=os.path.join(file_path,i)
        success_num+=len(os.listdir(path))
    print('共',success_num,'个文件')

if __name__ == "__main__":
    fail_statistic(r'D:/pic1/failure_path')
    success_statistic(r'D:/pic1/已处理完成')