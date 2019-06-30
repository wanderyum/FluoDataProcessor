import os
import pandas as pd

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
    
def agilent_extract_data_from_single_file(path):
    '''
    用以从单个.txt文件中提取荧光通道、孔道、荧光值等数据。
    参数:
        path:   字符串, 目标文件路径
    返回:
        D:      字典, 包含提取出的数据
        例如:
        D(字典) --- FAM(字典) --- A1(列表)
                 |             +- A2(列表)
                 | 
                 +- HEX(字典) --- A1(列表)
                               +- A2(列表)
    '''
    D = {}
    target_sample = None
    target_channel = None
    f = open(path, 'r')
    s = f.readline()
    labels = extract_labels(s)

    while(labels):
        target_sample = labels[0]
        target_channel = labels[1]
        if target_channel not in D:
            D[target_channel] = {}
        if target_sample not in D[target_channel]:
            D[target_channel][target_sample] = []
        s = f.readline()
        while(s != '\n'):
            v = extract_datum(s)
            D[target_channel][target_sample].append(v)
            s = f.readline()
        s = f.readline()
        labels = extract_labels(s)
    f.close()
    return D
    
def extract_labels(s):
    '''
    用以提取荧光通道和孔道编号。
    参数:
        s:  字符串, 待提取字符串
    返回:
        若字符串为\n则返回None;
        否则返回(孔道编号, 荧光通道)
    '''
    L = s.split('\t')
    L = L[0].split(',')
    if len(L) == 1:
        return None
    else:
        sample, channel = L[0].strip(), L[1].strip()
        return (sample, channel)

def extract_datum(s):
    '''
    用以提取数据。
    参数:
        s:  字符串, 待提取字符串
    返回:
        数据(整数数值)
    '''
    L = s.split('\t')
    return int(L[2])

def combine_dictionaries(D1, D2):
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

def save_by_channel(D, folder='.', name='result', prefix='', postfix='', index=False):
    '''
    用以按荧光通道分别保存为csv文件。
    参数:
        D:          字典, 待保存
        folder:     字符串, 目标目录
        name:       字符串, 文件名
        prefix:     字符串, 加在名称前用于区分文件
        postfix:    字符串, 加在名称后用于区分文件
        index:      布尔型, 是否保留序号
    返回:
        target:     字符串, 保存的文件的完整路径
    '''
    target_files = []
    for channel in D:
        df = pd.DataFrame(D[channel])
        
        file_name = os.path.join(folder, generate_name(name=name, channel=channel, prefix=prefix, postfix=postfix))
        
        df.to_csv(file_name, index=index)
        target_files.append(file_name)
    return target_files
    
def generate_name(name, channel, prefix, postfix):
    name = name + '-' + channel
    if prefix:
        name = prefix + '-' + name
    if postfix:
        name = name + '-' + postfix
    name = name + '.csv'
    return name

if __name__ == '__main__':
    print(help(get_file_names))
    fs = get_file_names(directory='./data', filter='.txt', order='time')
    print(fs)