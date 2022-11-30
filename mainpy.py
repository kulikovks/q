
import time
import sys
import os
import psutil
import re
import numpy as np
import pandas as pd
#from sqlalchemy import create_engine
#engine = create_engine("mssql+pyodbc:///?odbc_connect=DRIVER={SQL+Server};SERVER=;DATABASE=;UID=;PWD=")
##os.chdir(r'C:\\Users\\KKulikov\\Desktop\\S') #4work
os.chdir(f'/home/{os.environ["LOGNAME"]}/pydir')


global realtime; realtime = lambda: time.strftime('%W[w] %j[d] %a [%p %I-%M-%S]')


def papka(x=False, y=False):
    if not x and not y:
        print(f'{realtime()[-13:]}>> open: os.system(r"xdg-open " + {os.getcwd()})')
        os.system(r'xdg-open '+ os.getcwd())
    elif x and not y:
        if x == 1:
            empty_file = str(time.time_ns())
            print(f'{realtime()[-13:]}>> create: os.open({os.path.join(os.getcwd(), empty_file)}, os.O_CREAT)')
            os.open(empty_file, os.O_CREAT)
        else:
            print(f'{realtime()[-13:]}>> os.startfile({os.path.join(os.getcwd(), x)})')
            os.startfile(x)
    else:
        print(f'{realtime()[-13:]}>> {x}.replace({x}[{x}.rfind(".")],{y})')
        os.startfile(x.replace(x[x.rfind('.')],y))


def files (f=False):
    if not f:
        return {x:y for x, y in enumerate(os.path.join(os.getcwd(),j) for i, j in sorted([(os.path.getmtime(os.path.join(os.getcwd(), j)), j,) for i, j in [(i, j) for i, j in enumerate(os.listdir()) if os.path.isfile(os.path.join(os.getcwd(), str(j)))]], key = lambda x: x[0], reverse=True))}  
    else:
        return {x:y for x, y in enumerate(os.path.join(os.getcwd(),f, j) for i,j in sorted([(os.path.getmtime(os.path.join(os.getcwd(),f, j)), j,) for i, j in[(i, j) for i, j in enumerate(os.listdir(os.path.join(os.getcwd(),f))) if os.path.isfile(os.path.join(os.getcwd(),f, str(j)))]], key = lambda x: x[0], reverse=True))}


def sel(path=False):
    if not path:
        return {i:os.path.join(os.getcwd(),'select',_) for i,_ in enumerate(list(files('select')))}   
    else:
        return {i:os.path.join(os.getcwd(), 'select',path, _) for i,_ in enumerate(list(files(os.path.join(os.getcwd(),'select', path))))}


def reader(f, x='utf-8'):
    with open(f, mode = 'r', encoding=x) as _:
        f = _.read()
    return f  


def sql (s='', db='EGE',  y=22):
    dbo = f' [ERBD_{db}_MAIN_{str(y)}].dbo.'
    for i in set(re.findall(' dat_| res_| rbd_| rbdc_| ac_| sht_| sheets.', s, re.IGNORECASE)):
        if i == ' sheets.':
            s = s.replace(i, dbo[:-4]+i[1:])
            continue
        s = s.replace(i, dbo+i[1:])
    return s


def squeez(df, x = 0):
    try:
        assert isinstance(df.shape, tuple)
    except Exception as error:
        raise error
    if x >= 0:
        cols = {col: [['']]+[[np.float_(0)]] + [[np.float_(0)]] for col in df.columns.tolist()}
        print(f'{realtime()[-13:]}>>\n'
              f'{df.columns}\n'
              f'{np.around((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 6)} (MB)\n',)
        a = np.around((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 2)
    if np.int_(x) == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
    for i in range(df.shape[1]):
        if x >= 0:
            cols[df.columns[i]][1] = np.float_(cols[df.columns[i]][1][0]) + np.around(np.float_(df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 2)
        df[df.columns[i]] = df[df.columns[i]].convert_dtypes()
        if re.match('I', df[df.columns[i]].dtypes.name):
            df.isetitem(i, pd.to_numeric(df[df.columns[i]], downcast='integer'))
            if x >= 0:
                try:
                    cols[df.columns[i]][0] = df.convert_dtypes().iloc[0,i].dtype.name
                except Exception:
                    cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        elif re.match('F', df[df.columns[i]].dtypes.name):
            df.isetitem(i, pd.to_numeric(df[df.columns[i]], downcast='float'))
            if x >= 0:
                try:
                    cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
                except Exception:
                    cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        elif isinstance(x,float) and re.match('string', df[df.columns[i]].dtypes.name):
            df.isetitem(i, df[df.columns[i]].astype('category'))
            if x >= 0:
                try:
                    cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
                except Exception:
                    cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        else:
            if x >= 0:
                cols[df.columns[i]][2] = np.float_(cols[df.columns[i]][2][0]) + np.around(np.float_(df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 4)
                try:
                    cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
                except Exception:
                    cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
                continue
        if x >= 0:
            cols[df.columns[i]][2] = cols[df.columns[i]][2][0] + np.around(np.float_(df[df.columns[i]].memory_usage(deep=True) / 1024 ** 2), 2)
            try:
                cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
    if x >= 0:
        b = np.around((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 2)
    if np.int_(x) == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
        print(f'{realtime()[-13:]}>> profit: {a} - {b} = {a - b} (MB)\n-----')
        return df
    if x < 0:
        return df
    elif np.int_(x) == 0:
        print(f'{realtime()[-13:]}>> shape: {df.shape}')
        print(f'{realtime()[-13:]}>> profit: {a} - {b} = {a - b} (MB)\n-----')
        return {i: j for i, j in cols.items()}


def fkey (D, val):
    for i,_ in D.items():
        if _==val:
            return i


def attrs(x):
    return {i: {_:str(getattr(x, _))} for i,_ in enumerate(dir(x)) if _[0] != '_'}


def usage():
    return print(f'{psutil.Process(os.getpid())}\n'\
                 f'{psutil.Process(os.getpid()).memory_full_info()[1] / 1024**2}')


#pd.set_option('compute.use_numba', True)
pd.set_option('display.max_columns', 0) 
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_rows', 111)
pd.set_option('display.min_rows', 0)


print('psutil.Process(os.getpid())', 'psutil.Process(os.getpid()).memory_full_info()[1] / 1024**2', sep='\n')
usage()
print('\nsys.version: ', sys.version, sep='')
print(sys.hash_info)
print('sys.base_prefix: ', sys.base_prefix, '\n',sep='')
print(os.getcwd())
print(realtime())
print("pd.set_option('compute.use_numba', False)")
print("pd.set_option('display.max_rows', 111)")
print('''
# import matplotlib.pyplot as plt
# import seaborn as sns
# import statsmodels.api as sm 
# from statsmodels.stats.outliers_influence import variance_inflation_factor
# from sklearn import linear_model
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, r2_score
# -----
# import pyspark.pandas as ps
# import pyspark.sql.functions as F
# from pyspark.sql import SparkSession
# spark = SparkSession.builder.master('local[2]').appName('envI').getOrCreate()
# pth = f'/home/{os.environ["LOGNAME"]}/pydir/select/trtr'
# sparkdf = (
#     spark.read
#     .parquet(pth)
# )
''')
