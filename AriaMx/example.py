import os
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel
from dataviewer import dataViewer

folder = './data'

# 提取并合并数据
files = get_file_names(directory=folder, filter='.txt')

D = extract_data_from_single_file(os.path.join(folder, files[0]))

for f in files[1:]:
    D = combine_dictionaries(D, extract_data_from_single_file(os.path.join(folder,f)))

save_by_channel(D, folder=folder, name=files[0][:8], index=False)

# 可视化数据
target = get_file_names(directory=folder, filter='.csv', order='time')[0]
viewer = dataViewer()
viewer.import_data(path=os.path.join(folder, target))
viewer.mainloop()