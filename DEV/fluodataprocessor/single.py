import pandas as pd
import os

if __name__ == '__main__':
    import misc as m
else:
    import fluodataprocessor.misc as m
    
class singlefluoprocessor():
    def __init__(self):
        self.dir = None
        self.date = None
    
    def extract_data(self, directory, kind, channel, holes):
        '''
        用以提取文件中的数据，输出为？
        输入:
        directory:  字符串, 目标文件夹。
        kind:       字符串, 荧光机器型号, 如AriaMx/TL988。
        channel:    字符串'ALL'或包含所观察荧光通道的字符串列表。
        holes:      字符串'ALL'或包含所观察孔道的字符串列表。
        返回:
        若channel为'FAM'/'HEX'/'channel_0'/'channel_1'则返回DataFrame。
        若channel为'ALL'则返回以下格式的字典:
        D(字典) --- channel_0(DataFrame)
                 |      
                 -- channel_1(DataFrame)
        '''
        self.dir = directory

        res = None
        self.date = m.get_date(directory=directory, kind=kind)
        if kind.upper() == 'TL988':
            res = m.extract_data_TL988(directory=directory, channel=channel, holes=holes)
        elif kind.upper() == 'ARIAMX':
            # to be continued
            pass
        self.data = res
        return res
        
    def save_data(self, data=None, target_folder=None, name=None, index=False, preset=None):
        '''
        用来将DataFrame数据保存至csv文件中。
        输入:
        data:           DataFrame数据, 若未指定, 则采用singlefluoprocessor.data的数据。
        target_folder:  字符串, csv文件保存的文件夹, 若未指定, 则采用singlefluoprocessor.dir。
        name:           字符串, csv文件的文件名, 包含.csv。若未指定并且存在singlefluoprocessor.data, 否则采用result.csv。
        index:          布尔, 保存的csv文件是否包含索引, 默认不包含。
        preset:         字符串, 预设保存方式。默认将所有数据保存到一张csv中。
        '''

        if type(data) == type(None) and type(self.data) != type(None):
            data = self.data
        if type(target_folder) == type(None) and type(self.dir) != type(None):
            target_folder = self.dir
        if type(name) == type(None) and type(self.date) != type(None):
            name = self.date+'.csv'
        elif type(name) == type(None) and type(self.date) == type(None):
            name = 'result.csv'
        
        if type(data) == type({'a': 1}):
            if type(scheme) == type(None):
                for key in data:
                    data[key].to_csv(os.path.join(target_folder, key+'-'+name), index=index)
            elif scheme.upper() == 'MANFREDO':
                pass
        elif type(data) == type(pd.DataFrame([])):
            if type(preset) == type(None):
                data.to_csv(os.path.join(target_folder, name), index=index)
            elif preset.upper() == 'MANFREDO':
                lh = ['A3-10', 'B3-10', 'B13-20', 'A13-20']
                lp = ['-1', '-2', '-3', '-OneDay']
                for i in range(len(lh)):
                    holes = m.resolve_holes(lh[i])
                    data.to_csv(os.path.join(target_folder, name[:-4]+lp[i]+'.csv'), index=index, columns=holes)

if __name__ == '__main__':
    sfp = singlefluoprocessor()
    d = r'E:\Manfredo\ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20190929'
    target_holes = 'A3-10, A13-A20, B3-B10, B13-20'
    print(sfp.extract_data(d, 'TL988', 'Fam', target_holes))
    sfp.save_data(scheme='manfredo')
    #print(sfp.data)