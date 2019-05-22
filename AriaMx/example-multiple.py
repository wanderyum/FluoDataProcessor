
from misc import get_file_names

folder = 'data/multiple'

files = get_file_names(directory=folder, filter='.csv')
print(files)