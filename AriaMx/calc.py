import pandas as pd
import numpy as np

def align_data(arr, point=0):
    '''
    用以平移数据让多条荧光曲线在一个点重合到数值0。
    参数:
        arr:    ndarray, 待对齐数据
        point:  整数, 在第几个数据点对齐(从0开始计数)
    返回:
        arr:    ndarray, 对齐以后的数据
    '''
    for i in range(arr.shape[1]):
        arr[:,i] = arr[:,i] - arr[point, i]
    return arr
    
def cdecay(p, x):
    '''
    用以生成一条带一次方项的衰减的荧光值曲线。
    参数:
        p:  荧光衰减曲线参数, y = ax + b +c(d^x)
            p[0] - a
            p[1] - b
            p[2] - c
            p[3] - d
        x:  ndarray, 自变量取值
    返回:
        y:  ndarray, 衰减曲线
    '''
    a, b, c, d = p
    y = a*x + c*np.power(c, x) + b
    return y
    
print(type(np.array([1,2,3])))