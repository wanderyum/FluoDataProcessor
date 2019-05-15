import os

def get_file_names(directory='data', filter='.*'):
    '''
    用以返回目标路径中所有符合后缀的文件列表。
    参数:
        directory:  字符串, 数据所在目录地址
        filter:     字符串, 过滤出含有所需后缀的文件
    返回:
        字符串列表, 文件名组成的列表
    '''
    for root, dirs, files in os.walk(directory, topdown=False):
        pass
    
    if filter == '.*':
        return sort_names(files)
    else:
        res = []
        f_len = len(filter)
        for f in files:
            if f[-f_len:] == filter:
                res.append(f)
        return sort_names(res)
        
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
    
def extract_data_from_single_file(path):
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
        if target_sample not in D[target_fluo]:
            D[target_channel][target_sample] = []
        s = f.readline()
        while(s != '\n'):
            v = extract_datum(s)
            D[target_channel][target_sample].append(v)
            s = f.readline()
        s = f.readline()
        labels = extract_label(s)
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

if __name__ == '__main__':
    print(help(get_file_names))