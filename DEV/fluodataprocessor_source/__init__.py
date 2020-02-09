import sys
import os


__version__ = 0.486




######################
# Personal functions #
######################
def find_manfredo_folder():
    if sys.platform == 'linux':
        pass
    elif sys.platform == 'win32':
        for disk in ['C', 'D', 'E', 'F']:
            manfredo = 'Manfredo'
            if os.path.exists(os.path.join(disk+':\\', manfredo)):
                return os.path.join(disk+':\\', manfredo)
        else:
            raise Exception('Manfredo folder not found!')