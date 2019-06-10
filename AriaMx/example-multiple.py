import os
import numpy as np
import pandas as pd
from misc import get_file_names
from calc import cut_data, statistic_result, normalize_data_set
from dataviewer import dataViewer
import matplotlib.pyplot as plt

folder = 'data/multiple'
whether_plot = True
whether_sd = True
ratio = 4500 / 6800

files = get_file_names(directory=folder, filter='.csv')
data_set = []
for f in files:
    df = pd.read_csv(os.path.join(folder, f))
    data_set.append(np.array(df))

data_set = cut_data(data_set)
data_set = normalize_data_set(data_set)

mn, std = statistic_result(data_set)
labels = ['Neither', 'E', 'E+I3(0.0005)', 'E+I3(0.001)', 'E+I3(0.002)', 'E+I3(0.005)', 'E+I3(0.01)', 'E+I3(0.1)']
mn, std = ratio*mn, ratio*std
df = pd.DataFrame(mn, columns=labels)

if whether_plot == True:
    linewidth = 2
    n = mn.shape[0]
    x = np.linspace(0, n-1, n)
    plt.figure(figsize=(8,6))

    if whether_sd == False:
        for i in range(mn.shape[1]):
            plt.plot(x, nm[:,i], label=labels[i], linewidth=linewidth)
    else:
        for i in range(mn.shape[1]):
            plt.errorbar(x, mn[:,i],std[:,i], label=labels[i], linewidth=linewidth)

    plt.legend()
    plt.tight_layout()
    plt.show()
df.to_csv(os.path.join(folder, '..', 'multiple-mean.csv'), index=False)
df = pd.DataFrame(std, columns=labels)
df.to_csv(os.path.join(folder, '..', 'multiple-std.csv'), index=False)
'''
viewer = dataViewer()
viewer.import_data(from_data=True, df=df)
viewer.mainloop()
'''