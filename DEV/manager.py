import sys
import shutil
import os

class manager():
    def __init__(self):
        self.sp = None

    def find_sp(self):
        if sys.platform == 'win32':
            for item in sys.path[::-1]:
                if item[-13:] == 'site-packages':
                    return item
        elif sys.platform == 'linux':
            for item in sys.path[::-1]:
                if '/home/' in item and 'site-packages' in item and item[-13:] == 'site-packages':
                    return item
        
    def check_existence(self):
        print('Platform: {}'.format(sys.platform))
        sp = self.find_sp()
        if sp is None:
            print('Cannot find site-packages folder!')
            return False
        else:
            self.sp = sp
            print('Site-packages Folder:\n{}'.format(sp))
            if os.path.exists(os.path.join(sp, 'fluodataprocessor')):
                path_fdp = os.path.join(sp, 'fluodataprocessor')
                
                from fluodataprocessor import __version__ as present_version
                from fluodataprocessor_source import __version__ as this_version
                if float(present_version) > this_version:
                    print('Task terminated because the version in computer is newer!')
                    return
                print('Found FluoDataProcessor version {} installed:\n{}'.format(present_version, os.path.join(sp, 'fluodataprocessor')))
                
                print('\nWhat to do next?\n(U)pdate    (R)emove    (C)ancel')
                ans = input()
                if ans[0].lower() == 'u':
                    self.update()
                elif ans[0].lower() == 'r':
                    self.uninstall()
                else:
                    print('Task cancelled.')
            else:
                print('Cannot find FluoDataProcessor')
                print('\nWhat to do next?\n(I)nstall    (C)ancel')
                ans = input()
                if ans[0].lower() == 'i':
                    self.install()
                else:
                    print('Task cancelled.')
            
    def install(self, silenced=False):
        sp_path = self.find_sp()
        shutil.copytree('./fluodataprocessor_source', os.path.join(sp_path, 'fluodataprocessor'))
        if not silenced:
            from fluodataprocessor import __version__ as present_version
            print('Successfully installed FluoDataProcessor version {}! \nLocation:\n{}'.format(present_version, os.path.join(sp_path, 'fluodataprocessor')))

    def uninstall(self, silenced=False):
        sp_path = self.find_sp()
        shutil.rmtree(os.path.join(sp_path, 'fluodataprocessor'))
        if not silenced:
            print('Successfully uninstalled!')

    def update(self, silenced=False):
        sp_path = self.find_sp()
        self.uninstall(silenced=True)
        self.install(silenced=True)
        if not silenced:
            from fluodataprocessor import __version__ as present_version
            print('Successfully update FluoDataProcessor to version {}\nLocation:\n{}'.format(present_version, os.path.join(sp_path, 'fluodataprocessor')))





if __name__ == '__main__':
    
    m = manager()
    m.check_existence()


    '''
    this_path = '.'
    folder = 'fluodataprocessor'
    if os.path.exists(os.path.join(target_path, folder)):
        if get_version(os.path.join(this_path, folder)) > get_version(os.path.join(target_path, folder)):
            print('An old version of {} is found, to update it? (Y)es or (N)o.'.format(folder))
            s = input()
            if s.upper() == 'Y' or s.upper() == 'YES':
                shutil.rmtree(os.path.join(target_path, folder))
                shutil.copytree('./fluodataprocessor', os.path.join(target_path, folder))
                print('Old version removed and new version installed!')
    else:
        shutil.copytree('./fluodataprocessor', os.path.join(target_path, folder))
        print('{} installed!'.format(folder))
    '''
    