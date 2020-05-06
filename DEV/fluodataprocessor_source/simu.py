import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

def peek_data(data, labels=None, x=None):
    dim = len(data.shape)
    if dim == 1:
        l = data.shape[0]
    elif dim == 2:
        l, w = data.shape
    if labels is None:
        labels = ['Curve 1', 'Curve 2', 'Curve 3', 'Curve 4', 'Curve 5', 'Curve 6', 'Curve 7', 'Curve 8']

    if x is None:
        x = np.linspace(0, l-1, l)

    plt.figure()

    if dim == 1:
        plt.plot(x, data, label=labels[0])
    if dim == 2:
        for i in range(w):
            plt.plot(x, data[:, i], label=labels[i])

    plt.legend()
    plt.tight_layout()
    plt.show()

class reaction():
    def __init__(self, plot_conc_unit='uM'):
        self.equations = []         # 反应式
        self.rates = []             # 用于存储反应速率序列, 每个对应一个反应式
        self.rate_cons = {}         # 反应速率常数的字典, 具体值只能被指定
        self.rate_cons_sim = {}     # 反应速率常数的字典, 用于拟合
        self.reactants = {}         # 所有参与反应的物质(包括反应物和生成物)的字典
        self.sample_interval = 60   # 采样间隔(秒), 默认1分钟


    def add_equation(self, equ, rate_constant):
        self.equations.append([equ, rate_constant])

    def init(self, D):
        '''
        用于产生一条初始浓度设置。除用户指定物质浓度外, 其它都置0。
        输入:
        D: 字典, 用户指定浓度。
        输出:
        ini: 字典, 包含所有物质浓度的一条初始浓度设置。
        '''
        
        if len(self.reactants) == 0:
            self.count_reactants()
        ini = {}
        for key in self.reactants:
            ini[key] = 0
        for key in D:
            ini[key] = D[key]
        return ini

    def count_reactants(self):
        '''
        自动推导所需的反应物并初始化反应物变化序列，以及反应速率序列。
        '''
        l = []
        self.rates = []
        for item in self.equations:
            tmp = item[0].split('->')
            for i in tmp:
                l += i.split('+')
            self.rates.append(None)
            if item[1] not in self.rate_cons:
                self.rate_cons[item[1]] = None
        s = set(l)
        for item in s:
            self.reactants[item] = None

    def fit_results(self, inis, p0, targets, y, sample_interval=None):
        '''
        inis:               列表, 里面是初始条件，每个初始条件为一个字典。
        p0:                 字典, 猜测的参数的初始值。
        targets:            列表, 里面是代表要测量量的字符串。
        y:                  ndarray, 实际荧光数值
        sample_interval:    正数, 采样间隔(秒)
        '''
        if sample_interval:
            self.sample_interval = sample_interval
        self.count_reactants()
        self.gen_rate_cons_sim()
        p0 = self.dic2list(p0)
        self.targets = targets
        self.inis = inis
        plsq = leastsq(self.error_function, x0=p0, args=y)[0]
        print('Error:', np.sum(self.error_function(plsq, y)))
        return plsq
        
    def gen_rate_cons_sim(self):
        for item in self.rate_cons:
            if self.rate_cons[item] is None:
                self.rate_cons_sim[item] = None

    def dic2list(self, D):
        res = []
        for item in sorted(D.keys()):
            res.append(D[item])
        return res

    def error_function(self, p, data):
        '''
        用于计算模拟结果与实验数据的误差。
        输入:
        p:      实数列表, 
        '''
        tmp = sorted(self.rate_cons_sim.keys())
        for i in range(len(tmp)):
            self.rate_cons_sim[tmp[i]] = p[i]
        sim = self.react(ini=self.inis, targets=self.targets, steps=data.shape[0], sample_interval=self.sample_interval)
        mat_tmp = np.square(data.T-sim)
        res = np.sum(mat_tmp, axis=0)
        return res

    def react(self, ini, targets, steps, sample_interval=None):
        if sample_interval is None:
            sample_interval = self.sample_interval
        results = []
        for item in ini:
            self.take_reactions(item, steps=steps, sample_interval=sample_interval)
            result_tmp = self.reactants[targets[0]]
            for tar in targets[1:]:
                result_tmp += self.reactants[tar]
            results.append(result_tmp)
        return np.array(results)

    def take_reactions(self, ini, steps, sample_interval=None):
        '''
        以一种初始条件开始仿真, 结果存于self.rates, self.reactants中。
        输入:
        ini:                字典, 初始条件
        steps:              整数, 模拟数据点的数量
        sample_interval:    正数, 采样间隔(秒)
        返回:
        无
        '''
        if sample_interval is None:
            sample_interval = self.sample_interval
        self.count_reactants()
        self.set_ini(ini, steps)
        for i in range(steps-1):
            # 复制前一步参与反应物质的浓度到后一步
            self.reaction_init(i)
            # 根据各反应式增减参与反应物质的浓度
            self.take_one_step_reactions(i, sample_interval=sample_interval)

    def set_ini(self, ini, steps):
        for item in self.reactants:
            self.reactants[item] = np.linspace(0, 0, steps)
        for item in ini:
            self.reactants[item][0] = ini[item]
        for i in range(len(self.rates)):
            self.rates[i] = np.linspace(0, 0, steps-1)

    def reaction_init(self, present_step):
        for item in self.reactants:
            self.reactants[item][present_step+1] = self.reactants[item][present_step]

    def take_one_step_reactions(self, present_step, sample_interval):
        '''
        用以模拟一个时间点上的反应。反应结果直接在self.reactants(反应物变化)和self.rates(反应速率变化)中记录。
        输入:
        present_step:       整数, 当前时间点
        sample_interval:    正数, 采样间隔(秒), 例如采样间隔1分钟则为60
        返回:
        无
        '''
        k = 0
        for eq in self.equations:
            tmp = eq[0].split('->')
            reactants = tmp[0].split('+')
            products = tmp[1].split('+')
            if self.rate_cons[eq[1]]:
                cons = self.rate_cons[eq[1]]
            else:
                cons = self.rate_cons_sim[eq[1]]
            # 这里的反应速率常数(cons)的数值以每秒为单位
            rate = cons * sample_interval
            for item in reactants:
                rate *= self.reactants[item][present_step]
            # 在self.rates中记录反应速率
            self.rates[k][present_step] = rate
            # 在self.reactants中记录参与反应物质的浓度
            for item in reactants:
                self.reactants[item][present_step+1] = self.reactants[item][present_step+1]-rate
            for item in products:
                self.reactants[item][present_step+1] = self.reactants[item][present_step+1]+rate
            k += 1

    def set_rate_constant(self, rate_constant, value):
        self.rate_cons[rate_constant] = value