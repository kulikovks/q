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
#     import urllib
#     import sqlalchemy as sa
#     from sqlalchemy import create_engine
#     _s=urllib.parse(quote_plus('DRIVER={SQL server};SERVER=;UID=;PWD='))
#     cconn = create_engine('mssql+pyodbc:\\\?odbc_connect=%s'%_s)
import numpy as np
import matplotlib.pyplot as plt  # https://matplotlib.org/stable/api/figure_api.html
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots


def papka(x=False, y=False):
    if not x and not y:
        print(f'{realtime()[-13:]}>> open: os.system(r"explorer.exe " + {os.getcwd()})')
        os.system(r'explorer.exe ' + os.getcwd())
    elif x and not y:
        if x == 1:
            print(f'{realtime()[-13:]}>> create: os.open({os.getcwd()}'f'\\{str(time.time_ns())}, os.O_CREAT)')
            os.open(empty_file, os.O_CREAT)
        else:
            print(f'{realtime()[-13:]}>> os.startfile({os.getcwd()}'f'\\{x})')
            os.startfile(x)
    else:
        print(f'{realtime()[-13:]}>>{x}.replace({x}[{x}.rfind(".")],{y})')
        os.startfile(x.replace(x[x.rfind('.')], y))


def files(f=False):
    if not f:
        filelist = filter(lambda x: os.path.isfile(os.path.join(os.getcwd(), x)), os.listdir(os.getcwd()))
        filelist = sorted(filelist, key=lambda x: os.path.getmtime(os.path.join(os.getcwd(), x)), reverse=True)
        filelist = {i: j for i, j in enumerate(filelist)}
        return filelist
    else:
        filelist = filter(lambda x: os.path.isfile(
            os.path.join(os.getcwd() + '\\' + str(f), x)), os.listdir(str(os.getcwd()) + '\\' + str(f)))
        filelist = sorted(filelist, key=lambda x: os.path.getmtime(os.path.join(str(os.getcwd()) + '\\' + str(f), x)))
        filelist = {i: j for i, j in enumerate(filelist[::-1])}
        return filelist


def sel(path=False):
    if not path:
        return {i: os.getcwd() + '\\select\\' + _ for i, _ in enumerate(list(files('select').values()))}
    else:
        return {i: os.getcwd() + f'\\select\\{path}\\' + _ for i, _ in
                enumerate(list(files(f'select\\{path}').values()))}


def reader(f, x='utf-8'):
    with open(f, mode='r', encoding=x) as _:
        f = _.read()
        return f


def sql(s='', db='EGE', y=22):
    dbo = f' [ERBD_{db}_MAIN_{str(y)}].dbo.'
    for i in set(re.findall(' dat_| res_| rbd_| rbdc_| ac_| sht_', s, re.IGNORECASE)):
        s = s.replace(i, dbo + i[1:])
    return s


def usage():
    return print(f'{psutil.Process(os.getpid())}\n\n'f'{psutil.Process(os.getpid()).memory_full_info()}\n')


def fkey(D, val):
    # return (i for i,j in D.items() if j==val)
    for i, _ in D.items():
        if _ == val:
            return i


def squeez(df, x = 0, *args):  # x=1:printer; *dict()
    try:
        assert isinstance(df.shape, tuple)
    except Exception as error:
        raise error
    if not args:
        args = None
    cols = {col: [['']]+[[.0]] + [[.0]] for col in list(df.columns)}
    print(f'{realtime()[-13:]}>>\n'
          f'{type(df), round(float(df.memory_usage(deep=True).sum() / 1024 ** 2), 6)} (MB)\n',
          type(args))
    cnt = float(.0)
    a = round(float(df.memory_usage(deep=True).sum() / 1024 ** 2), 2)
    if x == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
    for i in range(df.columns.shape[0]):
        cols[df.columns[i]][1] = float(cols[df.columns[i]][1][0]) + round(float(
            df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 2)
        df.iloc[:, i] = df.convert_dtypes().iloc[:, i].values
        if re.match('I', df.iloc[:, i].dtypes.name):
            df.iloc[:, i] = pd.to_numeric(
                df.iloc[:, i].values, downcast='integer')
            try:
                cols[df.columns[i]][0] = df.convert_dtypes().iloc[0,i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        elif re.match('F', df.iloc[:, i].dtypes.name):
            df.iloc[:, i] = pd.to_numeric(
                df.iloc[:, i].values, downcast='float')
            try:
                cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
        else:
            cols[df.columns[i]][2] = float(cols[df.columns[i]][2][0]) + round(float(
                df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 4)
            cnt = cnt + \
                round(float(df.iloc[:, i].memory_usage(
                    deep=True) / 1024 ** 2), 4)
            try:
                cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
            except Exception:
                cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
            continue
        cols[df.columns[i]][2] = cols[df.columns[i]][2][0] + round(float(
            df.iloc[:, i].memory_usage(deep=True) / 1024 ** 2), 2)
        try:
            cols[df.columns[i]][0] = df.iloc[0, i].dtype.name
        except Exception:
            cols[df.columns[i]][0] = df.iloc[:, i].dtype.name
    b = round(float(df.memory_usage(deep=True).sum() / 1024 ** 2), 2)
    if x == 1:
        pd.DataFrame(df.info(memory_usage='deep'))
    if x < 0:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> profit {b - a} (MB)')
        {print(i, j) for i, j in cols.items()}
        return df
    elif not args and x == 0:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> profit {b - a} (MB)')
        {print(i, j) for i, j in cols.items()}
        return
    else:
        print(f'{realtime()[-13:]}>> shape -> {df.shape}')
        print(f'{realtime()[-13:]}>> before = {a} MB\n'
              f'{realtime()[-13:]}>> after = {b} MB (inc. <object> {cnt} MB)\n'
              f'{realtime()[-13:]}>> profit: {a - b} MB')
        return {i: j for i, j in cols.items()}


global file
file = lambda: str(time.time_ns()) + '.csv'

global realtime
realtime = lambda: time.strftime('%W[w] %j[d] %a [%p %I-%M-%S]')

C = lambda c: {i: _ for i, _ in enumerate(c.columns)}

print(sys.version)
print(sys.hash_info)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# os.chdir(r'C:\\Users\\KKulikov\\Desktop\\S') # 4work
os.chdir(r'D:\python\New folder')
