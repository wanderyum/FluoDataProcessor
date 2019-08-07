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

def ini_res():
    res = {}
    for let in ['A', 'B']:
        for i in range(3, 11):
            res[let+str(i)] = []

        for i in range(13, 21):
            res[let+str(i)] = []
    return res

def calibration_single_file(path, D, res):
    df = pd.read_csv(path)
    for let in ['A', 'B']:
        for i in range(3, 11):
            tmp = []
            tmp.append(df[let+str(i)][D[let+'3-10'][0][0]:D[let+'3-10'][0][1]].mean())
            tmp.append(df[let+str(i)][D[let+'3-10'][1][0]:D[let+'3-10'][1][1]].mean())
            res[let+str(i)]=tmp[1]-tmp[0]
        for i in range(13, 21):
            tmp = []
            tmp.append(df[let+str(i)][D[let+'13-20'][0][0]:D[let+'13-20'][0][1]].mean())
            tmp.append(df[let+str(i)][D[let+'13-20'][1][0]:D[let+'13-20'][1][1]].mean())
            res[let+str(i)]=tmp[1]-tmp[0]
    return res
