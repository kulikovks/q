import time
import sys
import os
import re
import psutil
# import pyodbc as dbc
# server = r'SERVER=;'
# user = r'UID=;'  # username
# pas = r'PWD='   # password
# conn = dbc.connect(r'Driver={SQL Server};'+server+user+pas)
import numpy as np
import matplotlib.pyplot as plt # https://matplotlib.org/stable/api/figure_api.html
import seaborn as sns
#sns.reset_defaults()
import pandas as pd
#trdf = pd.DataFrame(pd.np.random.randn(50000,300))
#pd.reset_option('all'); pd.reset_option('plotting.backend')
#print(pd.options.plotting.backend)
# dir(pd.options.plotting) ==> ['backend', 'matplotlib']
#pd.options.plotting.backend = "plotly"
#pd.reset_option('plotting.backend')
    # import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

def papka(x=False, y=False):
    if not x and not y:
        print(f'{realtime()[-13:]}>> open: os.system(r"explorer.exe " + {os.getcwd()})')
        os.system(r'explorer.exe '+ os.getcwd())
    elif x and not y:
        if x == 1:
            empty_file = str(time.time_ns())
            print(f'{realtime()[-13:]}>> create: os.open({os.getcwd()}'f'\\{empty_file}, os.O_CREAT)')
            os.open(empty_file, os.O_CREAT)
        else:
            print(f'{realtime()[-13:]}>> os.startfile({os.getcwd()}'f'\\{x})')
            os.startfile(x)
    else:
        print(f'{realtime()[-13:]}>>{x}.replace({x}[{x}.rfind(".")],{y})')
        os.startfile(x.replace(x[x.rfind('.')],y))
    

def files (f=False):
    if not f:
        filelist = filter(lambda x: os.path.isfile(os.path.join(os.getcwd(), x)), os.listdir(os.getcwd()))
        filelist = sorted(filelist, key = lambda x: os.path.getmtime(os.path.join(os.getcwd(), x)), reverse=True)
        filelist = {i: j for i, j in enumerate(filelist)}
        return filelist
    else:
        filelist = filter(lambda x: os.path.isfile(os.path.join(os.getcwd()+'\\'+str(f), x)), os.listdir(str(os.getcwd())+'\\'+str(f)))
        filelist = sorted(filelist, key = lambda x: os.path.getmtime(os.path.join(str(os.getcwd())+'\\'+str(f), x)))
        filelist = {i: j for i, j in enumerate(filelist[::-1])}
        return filelist


# sel = lambda: {i:os.getcwd() + '\\select\\'+_ for i,_ in enumerate(list(files('select').values()))}
def sel(path=False):
    if not path:
        return {i:os.getcwd() + '\\select\\'+_ for i,_ in enumerate(list(files('select').values()))}
    else:
        return {i:os.getcwd() + f'\\select\\{path}\\'+_ for i,_ in enumerate(list(files(f'select\\{path}').values()))}

def reader(f, x='utf-8'):
    with open(f, mode = 'r', encoding=x) as _:
        f = _.read()
    return f  

def sql (s='', db='EGE',  y=22):
    dbo = f' [ERBD_{db}_MAIN_{str(y)}].dbo.'
    for i in set(re.findall(' dat_| res_| rbd_| rbdc_| ac_| sht_', s, re.IGNORECASE)):
        s = s.replace(i, dbo+i[1:])
    return s

def usage():
    return print(f'{psutil.Process(os.getpid())}\n\n'f'{psutil.Process(os.getpid()).memory_full_info()}\n')

def fkey (D, val):
    res = {}
    for i,_ in D.items():
        if _==val:
            return i

def attrs(x):
    return {i:{_:str(getattr(x, _))} for i,_ in enumerate(dir(x))}

def squeez(df, x=0, **kwargs): # x=1:printer; **dict()
    cols = {col: [[.0]]+[[.0]] for col in list(df.columns)}
    print(f'{realtime()[-13:]}>> ',type(kwargs))
    if x == 1:
        cnt = float(.0)
        a=round(float(df.memory_usage(deep=True).sum()/1024**2),2)
        pd.DataFrame(df.info(memory_usage='deep'))
    for column in tuple(list(cols.items())[i][0] for i in range(len(cols))):
#         print(column)
        if x == 1 or isinstance(kwargs,dict):
            cols[column][0] = float(cols[column][0][0]) + round(float(df[column].memory_usage(deep=True)/ 1024**2),2)
        # main_loop
        if str(df[column]).count('int') > 0:
#             print('************************************************************"int")')
            df[column] = pd.to_numeric(df[column], downcast='integer')
        elif str(df[column]).count('float') > 0:
#             print('************************************************************"int\float")')
            df[column].fillna(value=0, method=None, inplace=True) # axis{0 or ‘index’, 1 or ‘columns’}
            df[column] = df[column].astype('int')
            if str(df[column]).count('float') > 0:
#                 print('************************************************************"float")')
                df[column] = pd.to_numeric(df[column], downcast='float')
                
#         elif float(len(df[column].unique()) / len(df[column])) < 0.85:
#             df[column] = df[column].astype('category')
        else:
            if x == 1 or isinstance(kwargs, dict):
                cols[column][1] = float(cols[column][1][0]) + round(float(df[column].memory_usage(deep=True)/ 1024**2),4)
                if x ==1:
                    cnt=cnt+round(float(df[column].memory_usage(deep=True)/ 1024**2),4) #not squeez
#                     print(f'>> <><><>\n'f'{column} can not be squeez\n'f'({df[column].memory_usage(deep=True)/ 1024**2} MB)\n'f'*****\n')
                continue
            #break
        if x == 1 or isinstance(kwargs, dict): #not squeez
            cols[column][1] = cols[column][1][0] + round(float(df[column].memory_usage(deep=True)/ 1024**2),2)
    if isinstance(kwargs, dict) and x == 0:
        kwagrs = {i:j for i,j in list(cols.items())}.copy()
        return kwagrs
    elif isinstance(kwargs, dict) and x == 1:
        b=round(float(df.memory_usage(deep=True).sum()/1024**2),2)
        pd.DataFrame(df.info(memory_usage='deep'))
        print(f'{realtime()[-13:]}>> before = {a} MB\n'f'{realtime()[-13:]}>> after = {b} MB   (include "object" type on {cnt} MB)\n'f'{realtime()[-13:]}>> profit: {a-b} MB\n'f'\n'f'{[*cols.items()]}')
        
        kwargs = {i:j for i,j in list(cols.items())}.copy()
        return kwargs
    elif x== 1:
        b=round(float(df.memory_usage(deep=True).sum()/1024**2),2)
        pd.DataFrame(df.info(memory_usage='deep'))
        print(f'{realtime()[-13:]}>> before = {a} MB\n'f'{realtime()[-13:]}>> after = {b} MB   (include "object" type on {cnt} MB)\n'f'{realtime()[-13:]}>> profit: {a-b} MB\n'f'\n'f'{[*cols.items()]}')

global file
file = lambda: str(time.time_ns()) + '.csv'
global realtime
realtime = lambda: time.strftime('%W[w] %j[d] %a [%p %I-%M-%S]')

C = lambda c: {i: _ for i,_ in enumerate(c.columns)}

print(sys.version)
print(sys.hash_info)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# os.chdir(r'C:\\Users\\KKulikov\\Desktop\\S') # 4work
os.chdir(r'D:\python\New folder')