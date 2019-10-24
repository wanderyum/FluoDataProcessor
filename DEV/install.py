import sys
import shutil
import os

if sys.platform == 'linux':
    os.chdir(os.path.dirname(sys.argv[0]))

def find_sitepackages():
    if sys.platform == 'win32':
        for item in sys.path[::-1]:
            if 'site-packages' in item:
                return item
    elif sys.platform == 'linux':
        for item in sys.path[::-1]:
            if '/home/' in item and 'site-packages' in item:
                return item
                
def get_version(path):
    with open(os.path.join(path, '__init__.py'), 'r') as f:
        line = f.readline()
        try:
            return float(line.split('version ')[-1])
        except:
            raise Exception('No version information!')

if __name__ == '__main__':
    print('Platform:\t\t{}'.format(sys.platform))
    target_path = find_sitepackages()
    print('Packages location:\t{}'.format(target_path))

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
        
    