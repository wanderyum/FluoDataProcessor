import os
import sys
import time
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel

sys.path.append('..')
from dataviewer import dataViewer

class data_extractor():
    def __init__(self, two_channel_path, output_folder='.', prefix='output', postfix=''):
        self.output_folder = output_folder
        self.prefix = prefix
        self.postfix = postfix
        self.two_channel_path = two_channel_path
        
    def extract(self, folder, sleep_time=1):
        self.get_dat_file(folder=folder, sleep_time=sleep_time)
        D = extract_data_from_single_file(os.path.join(folder, files[0]))
        for f in files[1:]:
            D = combine_dictionaries(D, extract_data_from_single_file(os.path.join(folder,f)))
        self.target_files = save_by_channel(D, folder=self.output_folder, name=files[0][:8], prefix=self.prefix, postfix=self.postfix, index=False)
        
    def get_dat_file(self, folder, sleep_time):
        pcr_file = get_file_names(folder, filter='.pcr')[0]
        cmd_run_TC = 'start /b '+self.two_channel_path+' '+os.path.join(folder, pcr_file)
        os.system(cmd_run_TC)
        time.sleep(sleep_time)
        pcr_name = pcr_file[:-4]
        cmd_copy = 'copy '+os.path.join(folder, '~'+pcr_name, pcr_name+'.dat')+' '+os.path.join(folder, pcr_name+'.dat')
        print(cmd_copy)
        os.system(cmd_copy)
        time.sleep(sleep_time)
        cmd_kill = 'taskkill /f /t /im TwoChannel.exe'
        os.system(cmd_kill)
        cmd_del = 'del /q '+os.path(folder, '~'+pcr_name, '*.*')+' & rd '+os.path.join(folder, '~'+pcr_name)
        print(cmd_del)
        os.system(cmd_del)
        

    def show_result(self):
        for f in self.target_files:
            viewer = dataViewer()
            viewer.load_csv(path=f, title=f)
            viewer.mainloop()