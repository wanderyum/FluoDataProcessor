import os
import sys
import pandas as pd
import numpy as np
from misc import get_file_names, extract_data_from_single_file, combine_dictionaries, save_by_channel
from calc import align_data, normalize_data
sys.path.append('..')
from dataviewer import dataViewer

folder = 'data/raw'
pfolder = os.path.join(folder, '..')
extract_label = 'extracted'
normalize_label = 'normalized'
align_point = 0

extract_data = True
#extract_data = False

process_data = True
process_data = False

view_data = True

# 提取并合并数据
if extract_data:
    files = get_file_names(directory=folder, filter='.txt')
    
    D = extract_data_from_single_file(os.path.join(folder, files[0]))

    for f in files[1:]:
        D = combine_dictionaries(D, extract_data_from_single_file(os.path.join(folder,f)))
    
    save_by_channel(D, folder=pfolder, name=files[0][:8], extra_label=extract_label, index=False)

# 处理数据
if process_data:
    files = get_file_names(directory=pfolder, filter='.csv', order='time')
    for f in files:
        if extract_label in f:
            target = f
            break
    print(target)
    df = pd.read_csv(os.path.join(pfolder, target))
    labels = df.columns
    #labels = ['None', 'No Enz.', 'Enz. 0.01', 'Enz. 0.02', 'Enz. 0.05', 'Enz. 0.075', 'Enz. 0.1', 'Enz. 0.2']
    d = align_data(np.array(df), align_point)
    p0 = [1,1,1,1]
    d = normalize_data(d, p0=p0, mode='cdecay', cut_data=True, point=align_point, show_base=True)
    df = pd.DataFrame(d, columns=labels)
    df.to_csv(os.path.join(pfolder, target[:-13]+normalize_label+'.csv'), index=False)

# 可视化数据
if view_data:

    target = get_file_names(directory=pfolder, filter='.csv', order='time')[0]
    path = os.path.join(pfolder, target)
    
    viewer = dataViewer()
    viewer.load_csv(path=path)
    viewer.mainloop()