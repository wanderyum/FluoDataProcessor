import sys
import shutil

print(sys.platform)
print(sys.path)

if __name__ == '__main__':
    if sys.platform == 'win32':
        p = None
        for item in sys.path:
            if 'site-packages' in item:
                print(item)