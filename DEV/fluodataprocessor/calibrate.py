
if __name__ == '__main__':
    import misc as m
else:
    import fluodataprocessor.misc as m

class calib():
    def __init__(self):
        pass
        
    def load_files(self, list_files):
        self.files = list_files
        
    def load_folder(self, folder):
        self.files = m.get_file_names(folder, filter='.csv')
        
    def compute_R(self, file_dir):
        pass
        
    def compute_alpha(self):
        pass



if __name__ == '__main__':
    data_folder = '.'
    output_folder = '.'
    cal = calib()
    cal.load_files()