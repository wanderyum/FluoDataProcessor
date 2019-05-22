import os
import pandas as pd
import numpy as np
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel
from calc import align_data, normalize_data
from dataviewer import dataViewer

folder = 'data/raw'
pfolder = os.path.join(folder, '..')
normalized_name = 'normalized.csv'
align_point = 23

#extract_data = True
extract_data = False

process_data = True
#process_data = False

view_data = True

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
    labels = df.columns
    d = align_data(np.array(df), align_point)
    p0 = [1,1,1,1]
    d = normalize_data(d, p0=p0, mode='cdecay', cut_data=True, point=align_point)
    df = pd.DataFrame(d, columns=labels)
    df.to_csv(os.path.join(pfolder, normalized_name), index=False)

# 可视化数据
if view_data:
    if process_data:
        target = normalized_name
        path = os.path.join(pfolder, target)
    else:
        target = get_file_names(directory=folder, filter='.csv', order='time')[0]
        path = os.path.join(folder, target)
    
    viewer = dataViewer()
    viewer.import_data(path=path)
    viewer.mainloop()