if __name__ == '__main__':
    import misc as m
else:
    import fluodataprocessor.misc as m
    
class singlefluoprocessor():
    def __init__(self):
        pass
    
    def extract_data(self, directory, kind, channel, holes):
        '''
        用以提取文件中的数据，输出为？
        输入:
        directory:  字符串, 目标文件夹。
        kind:       字符串, 荧光机器型号, 如AriaMx/TL988。
        channel:    字符串'ALL'或包含所观察荧光通道的字符串列表。
        holes:      字符串'ALL'或包含所观察孔道的字符串列表。
        输出:
        ???
        '''
        self.dir = directory
        res = None
        if kind.upper() == 'TL988':
            res = m.extract_data_TL988(directory=directory, channel=channel, holes=holes)
        elif kind.upper() == 'ARIAMX':
            pass
        self.data = res
        return res


if __name__ == '__main__':
    sfp = singlefluoprocessor()
    d = r'D:\Manfredo\ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20190929'
    target_holes = 'A3-12, B3-B12'
    print(sfp.extract_data(d, 'TL988', 'ALL', target_holes))
    #print(sfp.data)