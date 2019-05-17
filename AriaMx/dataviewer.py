#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog



matplotlib.use('TkAgg')

font = {'label': ('times', 14, 'roman'),
        'button': ('times', 18, 'bold')
        }

class dataViewer(tk.Tk):
    def __init__(self, from_data=False, df=None):
        super().__init__()
        self.wm_title('Data Viewer')
        self.protocol('WM_DELETE_WINDOW', self._quit)
        self.resizable(width=False, height=False)
        self.createCanvas()
        self.btn = {}
        #self.import_data(from_data=from_data, df=df)

    
    def import_data(self, path='data.csv', from_data=False, df=None):
        self.vars = {}
        self.btn = {}
        if from_data:
            self.df = df
        else: 
            self.df = pd.read_csv(path)
        self.labels = self.df.axes[1]
        self.set_color()
        self.tmp = np.asarray(self.df)
        self.length = self.tmp.shape[0]
        self.set_min_and_max(self.tmp)
        self.createWidget()

    def set_min_and_max(self, data):
        self.maximum = np.max(data)
        self.maximum = (self.maximum // 500 + 1) * 500
        self.minimum = np.min(data)
        self.minimum = (self.minimum // 500 ) * 500
    
    def set_color(self):
        self.color = {}
        for i in range(len(self.labels)):
            self.color[self.labels[i]] = 'C' + str(i)

    def createCanvas(self):
        fig = plt.figure(figsize=(8,6), dpi=100)
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas._tkcanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        #toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        #toolbar.update()
        self.rightframe = tk.Frame(master=self)

        ###
        self.rightframe.bind_all('<Control-o>', self.shortcuts)
        self.rightframe.pack(side=tk.RIGHT)

        self.btnpanel = tk.Frame(master=self.rightframe)
        self.btnpanel.pack(side=tk.TOP)
        tk.Button(master=self.btnpanel, font=font['button'], text='打开', command=self.openfile).pack(side=tk.LEFT)
        tk.Button(master=self.btnpanel, font=font['button'], text='退出', command=self._quit).pack(side=tk.LEFT)
        
        self.funcpanel = tk.Frame(master=self.rightframe)
        self.funcpanel.pack(side=tk.TOP)
        tk.Button(master=self.funcpanel, font=font['button'], text='反选', command=self.reverse).pack(side=tk.LEFT)
        
        self.datapanel = tk.Frame(master=self.rightframe)
        self.datapanel.pack(side=tk.TOP)
    
    def createWidget(self):
        self.Dic_frame = {}
        for key in self.labels:
            self.vars[key] = tk.IntVar()
            btn = tk.Checkbutton(master=self.datapanel, text=key, variable=self.vars[key], width=45, onvalue=1, offvalue=0, command=self.draw)
            self.btn[key] = btn
            btn.select()
            btn.config(font=font['label'])
            btn.pack(side=tk.TOP, anchor=tk.W)
        self.draw()

    def draw(self):
        x = np.linspace(0, self.length-1, self.length)
        self.ax.clear()
        for key in self.labels:
            if self.vars[key].get() > 0:
                y = np.asarray(self.df.loc[:,[key]]).reshape(-1)
                self.ax.plot(x, y, label=key, color=self.color[key])
        self.ax.set_ylim([self.minimum, self.maximum])
        self.ax.set_xlim([0,self.length])
        self.ax.legend()
        self.canvas.draw()

    def openfile(self):
        filename = filedialog.askopenfilename(title='打开csv文件', filetypes=[('csv文件', '*.csv'), ('All Files', '*')])
        if filename:
            for key in self.btn:
                print('destroy:',self.btn[key])
                self.btn[key].destroy()
            self.import_data(filename)
    
    def shortcuts(self, key):
        self.openfile()
    
    def reverse(self):
        for key in self.vars:
            if self.vars[key].get() == 1:
                self.btn[key].deselect()
            else:
                self.btn[key].select()
        self.draw()

    def _quit(self):
        self.quit()
        self.destroy()

if __name__ == '__main__':
    viewer = dataViewer()
    viewer.mainloop()
