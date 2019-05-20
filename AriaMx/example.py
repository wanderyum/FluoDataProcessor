import os
import pandas as pd
import numpy as np
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel
from calc import align_data
from dataviewer import dataViewer

folder = './data'
align_point = 16

#extract_data = True
extract_data = False

process_data = True
#process_data = False

view_data = True
#view_data = False

# 提取并合并数据
if extract_data:
    files = get_file_names(directory=folder, filter='.txt')
    
    D = extract_data_from_single_file(os.path.join(folder, files[0]))

    for f in files[1:]:
        D = combine_dictionaries(D, extract_data_from_single_file(os.path.join(folder,f)))
    
    save_by_channel(D, folder=folder, name=files[0][:8], index=False)

# 处理数据
if process_data:
    target = get_file_names(directory=folder, filter='.csv', order='time')[0]
    print(target)
    df = pd.read_csv(os.path.join(folder, target))
    ### labels
    d = align_data(np.array(df), align_point)
    df = pd.DataFrame(d)
    df.to_csv('result.csv', index=False)

# 可视化数据
if view_data:
    target = get_file_names(directory=folder, filter='.csv', order='time')[0]
    viewer = dataViewer()
    viewer.import_data(path=os.path.join(folder, target))
    viewer.mainloop()