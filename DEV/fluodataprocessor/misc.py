import os
import numpy as np
import pandas as pd

#################
# 通用函数-杂项 #
#################
def get_file_names(directory='data', filter='.*', order='default'):
    '''
    用以返回目标路径中所有符合后缀的文件列表。
    参数:
        directory:  字符串, 数据所在目录地址
        filter:     字符串, 过滤出含有所需后缀的文件
        order:      字符串, 排序依据。default, 按名称排序, 短的在前。time, 按时间排序。
    返回:
        字符串列表, 文件名组成的列表
    '''
    if not os.path.exists(directory):
        raise Exception('Target directory does not exist!')
    for root, dirs, files in os.walk(directory, topdown=False):
        pass
    res = []
    if filter == '.*':
        res = files
    else:
        f_len = len(filter)
        for f in files:
            if f[-f_len:] == filter:
                res.append(f)
    if order == 'default':
        return sort_names(res)
    elif order == 'time':
        return sort_names_by_time(res, directory=directory)
    else:
        return res
        
def sort_names(L):
    '''
    用以对列表中的文件进行排序, 长度短的排在前面。例如, a排在a1前。
    参数:
        L:      字符串列表, 待排序列表
    返回:
        res:    字符串列表, 排序后的列表
    '''
    res = sorted(L)
    res.sort(key=len)
    return res
    
def sort_names_by_time(L, directory='.'):
    '''
    用以对列表中的文件按修改时间进行排序, 最新的排在前面。
    参数:
        L:          字符串列表, 待排序列表
        directory:  字符串, 列表中文件所在目录
    返回:
        res:    字符串列表, 排序后的列表
    '''
    tmp = []
    for item in L:
        tmp.append(os.path.join(directory, item))
    tmp.sort(key=os.path.getmtime, reverse=True)
    res = []
    for item in tmp:
        res.append(item[len(directory)+1:])
    return res
    
def combine_dicts(D1, D2):
    '''
    用以按顺序合并两个字典内容。
    参数:
        D1: 待合并字典
        D2: 被合并字典
    返回:
        D1: 合并后的字典
    '''
    for channel in D1:
        for sample in D1[channel]:
            D1[channel][sample] += D2[channel][sample]
    return D1
    
def resolve_holes(description):
    '''
    用以通过给定孔道描述生成包含孔道的列表。例如, 输入"A1-3"则返回['A1','A2','A3']。
    输入:
    description:    字符串, 孔道孔道描述。
    返回:
    holes:          字符串列表, 包含各孔道的列表。
    '''
    if type(description) == type(''):
        holes = []
        if description.upper() == 'ALL':
            for i in range(1,25):
                res.append('A'+str(i))
                res.append('B'+str(i))
        else:
            items = description.replace(' ', '')
            items = items.split(',')
            for item in items:
                holes += resolve_string(item)
        return holes
    elif type(description) == type([]):
        return description
        
def resolve_string(s):
    if '-' in s:
        res = []
        first, second = s.split('-')
        letter = first[0]
        start = int(first[1:])
        for i in range(len(second)):
            if second[i] >= '0' and second[i] <= '9':
                for j in range(start, int(second[i:])+1):
                    res.append(letter+str(j))
                return res
    else:
        return [s]
    
def get_date(directory, kind):
    '''
    用以得到实验日期。
    输入:
    directory:  字符串, 数据文件所在文件夹路径。
    kind:       字符串, 类型，如TL988等。
    返回:
    若解析成功则返回类似20190101的字符串, 若失败返回None。
    '''
    if kind.upper() == 'TL988':
        fs = get_file_names(directory=directory, filter='.dat')
        try:
            int(fs[-1][:-4])
        except:
            return
        else:
            return fs[-1][:-4]
            
def df2dic(df):
    D = {}
    for key in df.columns:
        D[key] = np.array(df0[key])[0]
    return D

def find_sitepackages():
    '''
    用以寻找site-packages文件夹。
    返回:     字符串, site-packages文件夹路径
    '''
    import sys
    if sys.platform == 'win32':
        for item in sys.path[::-1]:
            if item[-13:] == 'site-packages':
                return item
    elif sys.platform == 'linux':
        for item in sys.path[::-1]:
            if '/home/' in item and 'site-packages' in item and item[-13:] == 'site-packages':
                return item

#################
# 通用函数-计算 #
#################
def find_inflection_point(arr2d, rate=0.3):
    l = arr2d.shape[1]
    if l < 5:
        return -1
    for i in range(l-4):
        mean_tmp = np.mean(arr2d[:, i:i+4], axis=1)
        for j in range(arr2d.shape[0]):
            if arr2d[j, i+4] > mean_tmp[j] * (1+rate):
                return i+3
            elif arr2d[j, i+4] < mean_tmp[j] * (1-rate):
                return i+3
    return -1


#################
# Calibrate函数 #
#################
def calc_coef(df):
    arr = np.array(df.iloc[:])
    #print(arr)
    sum_r = np.sum(arr, axis=1, keepdims=True)
    mx = np.max(sum_r)
    coef_r = sum_r / mx
    arr = arr / coef_r
    #print(arr)
    mean_c = np.mean(arr, axis=0, keepdims=True)
    if arr.shape[0] >= 3:
        pass # 计算标准误
    max_col = np.max(mean_c)
    coef_col = mean_c / max_col
    pdr = pd.DataFrame(coef_col, columns=df.columns)
    return pdr
    
def load_coef(channel, directory=None):
    if directory is None:
        directory = default_calib_dir()
    target = None
    fs = get_file_names(directory=directory, filter='.csv')
    for item in fs:
        if '-'+channel+'.' in item:
            target = os.path.join(directory, item)
    
    if target:
        df = pd.read_csv(target)
        df_coef = calc_coef(df)
        return df2dic(df_coef)
        
def compensate_data(df, preprocessed=False):
    '''
    用于对于数据进行测量误差补偿。
    输入:
    df:     DataFrame, 待补偿数据
    preprocessed:   布尔型, False代表未进行预处理, 需要进行预处理。
    '''
    pass
    
def default_calib_dir():
    return os.path.join(find_sitepackages(), 'fluodataprocessor')

#################
# TL988相关函数 #
#################
def extract_data_TL988(directory, channel, holes):
    '''
    用以从.dat文件中提取荧光数据, 返回为包含数据的字典。
    输入:
    directory:  字符串, 目标文件夹。
    channel:    字符串'ALL'或包含所观察荧光通道的字符串列表。
    holes:      字符串'ALL'或包含所观察孔道的字符串列表。
    返回:
    若channel为'FAM'/'HEX'/'channel_0'/'channel_1'则返回DataFrame。
    若channel为'ALL'则返回以下格式的字典:
    D(字典) --- channel_0(DataFrame)
             |      
             -- channel_1(DataFrame)
    '''
    D = {}
    names = []
    channel_0 = []
    channel_1 = []

    target_holes = resolve_holes(holes)
    print('Target holes:\n{}'.format(target_holes))
    fs = get_file_names(directory=directory, filter='.dat')
    with open(os.path.join(directory, fs[0]), 'r') as f:
        for i in range(23):
            f.readline()
        for i in range(48):
            n, c1, c2 = get_name_and_value(f)
            if n in target_holes:
                names.append(n)
                channel_0.append(c1)
                channel_1.append(c2)
    if channel.upper() == 'ALL':
        D['channel_0'] = pd.DataFrame(np.array(channel_0).T, columns=names).sort_index(axis=1,ascending=True)
        D['channel_1'] = pd.DataFrame(np.array(channel_1).T, columns=names).sort_index(axis=1,ascending=True)
        return D
    elif channel.upper() == 'FAM' or channel.upper() == 'CHANNEL_0':
        return pd.DataFrame(np.array(channel_0).T, columns=names).sort_index(axis=1,ascending=True)
    elif channel.upper() == 'HEX' or channel.upper() == 'CHANNEL_1':
        return pd.DataFrame(np.array(channel_1).T, columns=names).sort_index(axis=1,ascending=True)
    
def get_name_and_value(f):
    name_ = f.readline()
    name = name_[8:-2]
    for i in range(9):
        f.readline()
    CHANNEL_0 = parse_fluo(f.readline())
    CHANNEL_1 = parse_fluo(f.readline())
    f.readline()
    return name, CHANNEL_0, CHANNEL_1
    
def parse_fluo(s):
    data = s[11:-2]
    L_s = data.split(',')
    L = []
    for datum in L_s:
        L.append(int(datum))
    return L
    
if __name__ == '__main__':
    #print(resolve_string('B2-5'))
    df = pd.read_csv(r'C:\Users\admin\AppData\Local\Programs\Python\Python36\Lib\site-packages\fluodataprocessor\calib-channel_1.csv')
    df0 = calc_coef(df)
    print(df0,'\n')

    print(load_coef('channel_1'))
    