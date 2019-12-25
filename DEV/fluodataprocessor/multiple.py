import numpy as np
import pandas as pd
import os

if __name__ == '__main__':
    import misc as m
else:
    import fluodataprocessor.misc as m
    
class multiplefluoprocessor():
    def __init__(self):
        self.dir = None
        self.date = None
        self.data = None
        self.labels = None
        self.aligned_data = None
        
    def process_folder(self, folder_path, filters=[], label_match_check=True):
        res = []
        for item in os.listdir(folder_path):
            if item[-4:] == '.csv':
                for filter in filters:
                    if filter not in item:
                        break
                else:
                    res.append(os.path.join(folder_path, item))
        return self.process_list(res, label_match_check=label_match_check)
        
    def process_list(self, files_list, label_match_check=True):
        self.load_list(files_list, label_match_check=label_match_check)
        self.align_data()
        data_mean = np.mean(self.aligned_data, axis=0)
        data_std = np.std(self.aligned_data, axis=0)
        data_se = data_std / np.sqrt(self.aligned_data.shape[0])
        return data_mean, data_se
        
    def load_list(self, files_list, label_match_check=True):
        self.data = []
        for file in files_list:
            df = pd.read_csv(file)
            if self.labels is None:
                self.labels = list(df.columns)
            elif label_match_check and self.labels != list(df.columns):
                self.data = None
                self.labels = None
                raise Exception('Abort: Labels do not match!')
            print('Loading data: {}'.format(file))
            self.data.append(np.array(df.iloc[:]))
            
    def align_data(self):
        '''
        用以对齐数据(使数据shape一致)。
        '''
        min_ = 10000
        for arr in self.data:
            if arr.shape[0] < min_:
                min_ = arr.shape[0]
        tmp = []
        for i in range(len(self.data)):
            tmp.append(self.data[i][:min_,:])
        self.aligned_data = np.array(tmp)

        
    
if __name__ == '__main__':
    mfp = multiplefluoprocessor()
    #mfp.process_list()
    data_mean, data_se = mfp.process_folder(r'D:\Manfredo\ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20191222', 
                                            filters = ['calib', 'channel_1'],
                                            label_match_check=False)
    import matplotlib.pyplot as plt
    plt.figure()
    x = np.arange(data_mean.shape[0])
    for i in range(data_mean.shape[1]):
        plt.errorbar(x, data_mean[:, i], yerr=data_se[:, i])
    plt.show()
    
    