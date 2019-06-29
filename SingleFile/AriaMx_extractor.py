import os
import sys
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel


sys.path.append('..')
from dataviewer import dataViewer

class data_extractor():
    def __init__(self, output_folder='.', prefix='output', postfix=''):
        self.output_folder = output_folder
        self.prefix = prefix
        self.postfix = postfix
        
    def extract(self, folder):
        files = get_file_names(folder)
        D = extract_data_from_single_file(os.path.join(folder, files[0]))
        for f in files[1:]:
            D = combine_dictionaries(D, extract_data_from_single_file(os.path.join(folder,f)))
        self.target_files = save_by_channel(D, folder=self.output_folder, name=files[0][:8], prefix=self.prefix, postfix=self.postfix, index=False)
    
    def show_result(self):
        for f in self.target_files:
            viewer = dataViewer()
            viewer.load_csv(path=f, title=f)
            viewer.mainloop()

if __name__ == '__main__':
    de = data_extractor()
    de.extract('raw_data')
    print(de.target_files)
    de.show_result()
    