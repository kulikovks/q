 
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
os.chdir(r'/home/q/snake')


global realtime
realtime = lambda: time.strftime('%W[w] %j[d] %a [%p %I-%M-%S]')


def papka(x=False, y=False):
    if not x and not y:
        print(f'{realtime()[-13:]}>> open: os.system(r"explorer.exe " + {os.getcwd()})')
        os.system(r'explorer.exe '+ os.getcwd())
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
        return [j for i, j in sorted([(os.path.getmtime(os.path.join(os.getcwd(), j)), j,) for i, j in [(i, j) for i, j in enumerate(os.listdir()) if os.path.isfile(os.path.join(os.getcwd(), str(j)))]], key = lambda x: x[0], reverse=True)]	
    else:
        return [j for i, j in sorted([(os.path.getmtime(os.path.join(os.getcwd(),f, j)), j,) for i, j in[(i, j) for i, j in enumerate(os.listdir(os.path.join(os.getcwd(),f))) if os.path.isfile(os.path.join(os.getcwd(),f, str(j)))]], key = lambda x: x[0], reverse=True)]


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


def squeez(df, x = 0, *args):  # x=1:printer; *dict()
    try:
        assert isinstance(df.shape, tuple)
    except Exception as error:
        raise error
    if not args:
        args = None
    cols = {col: [['']]+[[np.float_(0)]] + [[np.float_(0)]] for col in list(df.columns)}
    print(f'{realtime()[-13:]}>>\n'
          f'{type(df), round((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 6)} (MB)\n',
          type(args))
    cnt = np.float_(0)
    a = round((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 2)
    if x == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
    for i in range(df.columns.shape[0]):
        cols[df.columns[i]][1] = np.float_(cols[df.columns[i]][1][0]) + round(np.float_(
            df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 2)
        df.iloc[:, i] = df.convert_dtypes().iloc[:, i].values
        if re.match('I', df.iloc[:, i].dtypes.name):
            df.iloc[:, i] = pd.to_numeric(df.iloc[:, i].values, downcast='integer')
            try:
                cols[df.columns[i]][0] = df.convert_dtypes().iloc[0,i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        elif re.match('F', df.iloc[:, i].dtypes.name):
            df.iloc[:, i] = pd.to_numeric(df.iloc[:, i].values, downcast='float')
            try:
                cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        else:
            cols[df.columns[i]][2] = np.float_(cols[df.columns[i]][2][0]) + round(np.float_(
                df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 4)
            cnt = cnt + \
                round(np.float_(df.iloc[:, i].memory_usage(
                    deep=True) / 1024 ** 2), 4)
            try:
                cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
            continue
        cols[df.columns[i]][2] = cols[df.columns[i]][2][0] + round(np.float_(
            df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 2)
        try:
            cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
        except Exception:
            cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
    b = round((df.memory_usage(deep=True).sum().squeeze().astype(np.float_) / 1024 ** 2).astype(np.float_), 2)
    if x == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
    if x < 0:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> profit: {a - b} (MB)')
        {print(i, j) for i, j in cols.items()}
        return df
    elif not args and x == 0:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> profit: {a - b} (MB)')
        {print(i, j) for i, j in cols.items()}
        return
    else:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> before: {a} MB\n'
              f'{realtime()[-13:]}>> after: {b} MB (inc. <object> {cnt} MB)\n'
              f'{realtime()[-13:]}>> profit: {a - b} MB')
        return {i: j for i, j in cols.items()}


def fkey (D, val):
    for i,_ in D.items():
        if _==val:
            return i


def attrs(x): # словарь атрибутов ()
    return {i: {_:str(getattr(x, _))} for i,_ in enumerate(dir(x)) if _[0] != '_'}


def usage():
    return print(f'{psutil.Process(os.getpid())}\n'\
                 f'{psutil.Process(os.getpid()).memory_full_info()[1] / 1024**2}')


#pd.set_option('compute.use_numba', True)
pd.set_option('display.max_columns', 0) 
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_rows', 1111)
pd.set_option('display.min_rows', 0)
#pd.set_option('display.html.border', 1)


print('psutil.Process(os.getpid())', 'psutil.Process(os.getpid()).memory_full_info()[1] / 1024**2', sep='\n')
#print(f'{usage()}\n')
usage()
print('\nsys.version: ', sys.version, sep='')
print(sys.hash_info, '\n')
print(os.getcwd())
print(realtime())
print("pd.set_option('compute.use_numba', False)")
print("pd.set_option('display.max_rows', 1111)")
print('''
# import pyspark.pandas as ps
# import pyspark.sql.functions as F
# from pyspark.sql import SparkSession

# spark = SparkSession.builder.master('local[2]').appName('envI').getOrCreate()
# pth = r'/home/q/snake/select/trtr'
# sparkdf = (
#     spark.read
#     .parquet(pth)
# )
''')
