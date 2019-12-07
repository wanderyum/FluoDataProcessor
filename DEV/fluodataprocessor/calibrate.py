import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    import misc as m
else:
    import fluodataprocessor.misc as m

class calib():
    def __init__(self):
        pass
        
    def load_files(self, list_files):
        self.files = list_files
        
    def load_folder(self, folder, key=None):
        if key is None:
            tmp = m.get_file_names(folder, filter='.csv')
            self.files = []
            for item in tmp:
                self.files.append(os.path.join(folder, item))
        else:
            tmp = m.get_file_names(folder, filter='.csv')
            self.files = []
            for item in tmp:
                if key in item:
                    self.files.append(os.path.join(folder, item))
        return self.files    
        
    def compute_R(self, file_dir, inflection_point=None):
        arr = pd.read_csv(file_dir)
        np_arr = np.array(arr).T
        if inflection_point is None:
            inflection_point = m.find_inflection_point(np_arr)
        start_points = np_arr[:, inflection_point]
        end_points = np.mean(np_arr[:, -10:], axis=1)
        res = end_points-start_points
        return pd.DataFrame(res.reshape(1, -1), columns=arr.columns)
        
    def compute_alpha(self, folders, channel='channel_0'):
        if len(folders) == 0:
            raise Exception('Empty folders!')
        res = pd.DataFrame([])
        for folder in folders:
            fs = self.load_folder(folder, key=channel)
            res_tmp = pd.DataFrame([])
            for f in fs:
                df_tmp = self.compute_R(f)
                res_tmp = pd.concat([res_tmp, df_tmp], axis=1)
            res = pd.concat([res, res_tmp])
            #res = res[sorted(res.columns)]
        return res
            

    def calib(self, list_source_folders, channel='channel_0', directory=None):
        if directory is None:
            print(m.find_sitepackages())
            directory = m.default_calib_dir()
        print('Directory:\t{}'.format(directory))
        df = self.compute_alpha(list_source_folders, channel=channel)
        df.to_csv(os.path.join(directory, 'calib-'+channel+'.csv'), index=False)
    
    def show_bar_plot(self, channel, directory=None):
        if directory is None:
            directory = m.default_calib_dir()
        if os.path.exists(os.path.join(directory, 'calib-'+channel+'.csv')):
            df = pd.read_csv(os.path.join(directory, 'calib-'+channel+'.csv'))
            arr = df.iloc[:]
            arr_mean = np.mean(arr, axis=0)
            arr_std = np.std(arr, axis=0)
            arr_se = arr_std / np.sqrt(arr.shape[0])
            
            ind = np.arange(len(df.columns))
            width = 0.4
            
            plt.figure()

            plt.bar(ind, arr_mean, width, yerr=arr_se)
            plt.ylabel('Fluorescence intensity (a.u.)')
            plt.title('Calibration: {}'.format(channel))
            plt.xticks(ind, df.columns)
            
            plt.show()
            
        else:
            raise Exception('No calibrate file!')
        
        

if __name__ == '__main__':
    #data_folder = r'E:\Manfredo\ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20191112-std'
    output_folder = '.'
    cal = calib()
    '''
    mfolder = r'E:\Manfredo'
    folder1 = os.path.join(mfolder, r'ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20191112-std')
    folder2 = os.path.join(mfolder, r'ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20191115-std')
    folder3 = os.path.join(mfolder, r'ScientificResearch\PolymeraseDisplacement\ExperimentalData\Fluo\20191202-std')
    tmp = [folder1, folder2, folder3]
    cal.calib(tmp, channel='channel_1')
    '''
    cal.show_bar_plot(channel='channel_1')
    