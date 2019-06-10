import pandas as pd
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

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
        x:  ndarray(1D), 自变量取值
    返回:
        y:  ndarray(1D), 衰减曲线
    '''
    a, b, c, d = p
    y = a*x + c*np.power(d, x) + b
    return y
    
def fit_data(x, y, p0=None, mode='cdecay'):
    '''
    用以对实验数据进行拟合。
    参数:
        x:      ndarray(1D), 自变量取值
        y:      ndarray(1D), 实验数据
        p0:     列表, 初始参数取值
        mode:   字符串, 拟合模式。 可选:
                - cdecay, 带一次项的衰减曲线(默认)
    返回:
        plsq:           列表, 拟合得到的参数值
        fitted_data：    ndarray(1D), 拟合得到的曲线
    '''
    
    if mode == 'cdecay':
        if not p0:
            p0 = np.ones(4)
        def func_error(p, y):
            return y - cdecay(p, x)
        def get_fitted_data(p, x):
            return cdecay(p, x)
    else:
        raise Exception('Unknown mode name: {}'.format(mode))
    
    plsq = leastsq(func_error, p0, args=(y))[0]
    fitted_data = get_fitted_data(plsq, x)
    return (plsq, fitted_data)
    
def normalize_data(arr, p0=None, mode='cdecay', cut_data=False, point=0, show_base=False):
    '''
    用以拟合出基准曲线并令每条荧光曲线减去基准曲线。
    参数:
        arr:        ndarray, 待标准化数据
        p0:         列表, 初始参数取值
        mode:       字符串, 拟合模式。见fit_data函数。
        cut_data:   布尔型, 是否截取数据。比如结果截取第point个数据点之后的数据。
        point:      整数, 数据点。截取的起始点(序号从0开始, 截取时包括这个点)
        show_base:  布尔型, 是否显示基准曲线与拟合曲线对比。
    返回:
        arr:        ndarray, 标准化后的数据
    '''
    if cut_data:
        arr = arr[point:,:]
    r,c = arr.shape
    x = np.linspace(0, r-1, r)
    col = arr[:,0]
    p, base = fit_data(x, col, p0=p0, mode=mode)
    if show_base:
        compare_two_line(x, col, base)
    for i in range(c):
        arr[:,i] = arr[:,i] - base
    return arr
      
def compare_two_line(x, y, y_hat, figsize=(8,6)):
    '''
    用以对比实验曲线和拟合曲线差异。
    参数:
        x:          ndarray(1D), 自变量取值
        y:          ndarray(1D), 实验数据
        y_hat:      ndarray(1D), 拟合数据
        figsize:    元组, 图片尺寸
    返回:
        None
    '''
    plt.figure(figsize=figsize)
    plt.plot(x, y, label='y', color='C0', linewidth=1)
    plt.plot(x, y_hat, label='y_fit', color='C1', linewidth=1)
    plt.legend()
    plt.show()
    
def cut_data(L, point=None):
    res = []
    if point:
        for arr in L:
            res.append(arr[:point,:])
    else:
        min_r = L[0].shape[0]
        for arr in L:
            r, c = arr.shape
            if r < min_r:
                min_r = r
        for arr in L:
            res.append(arr[:min_r,:])
    return res
    
def statistic_result(L):
    n = len(L)
    data_matrix = L[0]
    for arr in L[1:]:
        data_matrix = np.hstack([data_matrix, arr])
    m = data_matrix.shape[1] // n
    L_mean = []
    L_std = []
    for i in range(m):
        tmp = data_matrix[:,i::m]
        L_mean.append(np.mean(data_matrix[:,i::m], axis=1, keepdims=True))
        L_std.append(np.std(data_matrix[:,i::m], axis=1, keepdims=True))
    matrix_mean = L_mean[0]
    matrix_std = L_std[0]
    for i in range(1, m):
        matrix_mean = np.hstack([matrix_mean, L_mean[i]])
        matrix_std = np.hstack([matrix_std, L_std[i]])
        
    return matrix_mean, matrix_std
    
def normalize_data_set(L):
    auxi = []
    for arr in L:
        auxi.append(np.sum(arr))
    mx = max(auxi)
    for i in range(len(auxi)):
        L[i] = L[i] * mx / auxi[i]
    return L

if __name__ == '__main__':
    a = np.array([1,5,1,5]).reshape((2,2))
    b = np.array([2,6,2,6]).reshape((2,2))
    c = np.array([3,7,3,7]).reshape((2,2))
    d = [a,b,c]
    print(a)
    print(b)
    print(c)
    mn, std = statistic_result(d)
    print(mn)
    print(std)

    '''
    x = np.linspace(0, 15, 16)
    x = x.reshape((2,8))
    print(x)
    column = x[:,0]
    x[:,0] = column*2
    print(x)
    print(x.shape)
    '''
    '''
    x = np.linspace(0, 99, 100)
    print('x shape:', x.shape)
    pp = [3,20,1,1.01]
    y = cdecay(pp, x)
    print('y shape:', y.shape)
    p0 = [-1,10,1,1]
    p = fit_data(x, y, p0)
    print('p:', p)
    plt.figure(figsize=(8,6))
    plt.plot(x, cdecay(p, x), label='y_fit', color='C0', linewidth=1)
    plt.plot(x, cdecay(pp, x), label='y', color='C1', linewidth=1)
    plt.legend()
    plt.show()
    '''