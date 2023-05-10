import os, sys, time, re
import numpy as np
import pandas as pd


global realtime
realtime = lambda: time.strftime('%W[w] %j[d] %a [%p %I-%M-%S]')


if re.match('win.', sys.platform):
    os.chdir(f"{os.environ['USERPROFILE']}\\pydir")
elif re.match('.inu.', sys.platform):
    os.chdir(f"/home/{os.environ['LOGNAME']}/pydir")
else:
    print('!!! use default directory\n\t=======')


try:
    try:
        from etcshadow import *
    except Exception as error:
        print(error)
    assert isinstance(SERVER, str)
    assert isinstance(DATABASE, str)
    assert isinstance(UID, str)
    assert isinstance(PWD, str)
    
    from sqlalchemy import create_engine
    engine = create_engine(
        "mssql+pyodbc:///?odbc_connect=DRIVER=[SQL+Server];SERVER={server};DATABASE={database};UID={uid};PWD={pwd}"
        .format(
            server=SERVER,
            database=DATABASE,
            uid=UID,
            pwd=PWD
        ).replace('[','{').replace(']','}')
    )
except NameError as error:
    print('from (SERVER, DATABASE, UID, PWD):\n\t%s\ncreate_engine from sqlalchemy not in use\n' % error)


def papka(x:(bool,str,int)=False) -> (None, float):
    '''
    open directory (x=False)
    -------
    if x is int then create empty .txt and return his name
    if x is string then get or create  x  file (return None)
    ---
    papka(papka(1)) # open empty .txt
    papka(papka('filename.py')) # create 'filename.py' and open directory
    papka(files(papka('filename.py'))[0]) # create and open 'filename.py'
    '''
    if not x:
        if re.match('.inu.', sys.platform):
            print(f'{realtime()[-13:]}>> open: os.system(r"xdg-open " + {os.getcwd()})')
            os.system(r'xdg-open '+ os.getcwd())
            return 
        else:
            print(f'{realtime()[-13:]}>> open: os.system(r"explorer.exe " + {os.getcwd()})')
            os.system(r'explorer.exe '+ os.getcwd())
            return 
    elif x:
        if isinstance(x, int):
            empty_file = str(time.time_ns()) + '.txt'
            print(f'{realtime()[-13:]}>> create: {os.path.join(os.getcwd(), empty_file)}')
            with open(empty_file, 'w'):
                pass
            return empty_file
        elif isinstance(x, str):
            try:
                os.startfile(x)
            except Exception as err:
                with open(x, 'w'):
                    pass
                return
            print(f'{realtime()[-13:]}>> os.startfile({os.path.join(os.getcwd(), x)})')
            return
        else: 
            return -0.1


def files(f:(bool, str)=False) -> dict:
    '''
    return dict-files ordered by descending last time change
    -------
    files('/home/pydir/downloads')
    '''
    if not f:
        return {x:y for x, y in enumerate(os.path.join(os.getcwd(),j) for i, j in sorted([(os.path.getmtime(os.path.join(os.getcwd(), j)), j,) for i, j in [(i, j) for i, j in enumerate(os.listdir()) if os.path.isfile(os.path.join(os.getcwd(), str(j)))]], key = lambda x: x[0], reverse=True))}  
    else:
        return {x:y for x, y in enumerate(os.path.join(os.getcwd(),f, j) for i,j in sorted([(os.path.getmtime(os.path.join(os.getcwd(),f, j)), j,) for i, j in[(i, j) for i, j in enumerate(os.listdir(os.path.join(os.getcwd(),f))) if os.path.isfile(os.path.join(os.getcwd(),f, str(j)))]], key = lambda x: x[0], reverse=True))}


def sel(path:str=False) -> dict:
    '''
    return dict-files ordered by descending last time change
    -------
    sel('20220131')
    '''
    if not path:
        return {i:os.path.join(os.getcwd(),'select',_) for i,_ in enumerate(list(files('select').values()))}   
    else:
        return {i:os.path.join(os.getcwd(), 'select',path, _) for i,_ in enumerate(list(files(os.path.join(os.getcwd(),'select', path)).values()))}


def reader(f:str, x:str='utf-8') -> str:
    '''
    read file with encoding
    -------
    f: filepath
    x: encoding
    '''
    with open(f, mode = 'r', encoding=x) as _:
        f = _.read()
    return f  


def squeez(
    df:pd.core.frame.DataFrame,
    x:(int,float)=0
) -> (None,dict,pd.core.frame.DataFrame):
    '''
    convert dtypes with downcast
    -------
    if 0 <= x < 1 then print short info and return dict-dtypes
    if x < 0 then no return (silence)
    if x >= 1 then print full info and return deep copy
    for convert string in category use floating point numbers
    '''
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
    if x >= 1:
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
    if x >= 1:
        pd.DataFrame(df.info(memory_usage='deep'))
        print(f'{realtime()[-13:]}>> profit: {a} - {b} = {a - b} (MB)\n-----')
        return df.copy(deep=True)
    if x < 0:
        return
    elif x >= 0:
        print(f'{realtime()[-13:]}>> shape: {df.shape}')
        print(f'{realtime()[-13:]}>> profit: {a} - {b} = {a - b} (MB)\n-----')
        return {i: j for i, j in cols.items()}


def fkey(D:dict, val):
    """
    find item index in dict
    -------
    fkey({0: 'a', 1: 'b'}, 'b')
    # return 1 (int)
    """
    for i, _ in D.items():
        if _ == val:
            return i


def attrs(x) -> dict:
    '''
    funny getter for classes or modules (without ` __ ` methods)
    -------
    attrs(plt.figure())
    attrs(pd.options)
    attrs(plt)[93]
    '''
    return {i: (_, str(getattr(x, _))) for i,_ in enumerate(dir(x)) if _[0] != '_'}


def quant(
    Series:(pd.core.series.Series, np.ndarray),
    top:int=75,
    bot:int=25,
    p:float=1.5,
    v:bool=False
) -> (pd.core.indexes.numeric.Int64Index, np.ndarray):
    '''
    return outliers from ` Series `
    (if Q-bot >= values >= Q-top
    -------
    p: multiplier for intr_qr 
    (p->max for extend range)
    # top_values = q75 + (p * intr_qr)
    # bot_values = q25 - (p * intr_qr)
    '''
    q_top, q_bot = np.percentile(Series, [top,bot])
    intr_qr = q_top - q_bot
    top_values = q_top + (p * intr_qr)
    bot_values = q_bot - (p * intr_qr)
    out_top = Series >= top_values
    out_bot = Series <= bot_values
    if v:
        print(f'Q-{top} (top): {q_top}, out Q (top): {_max},\nQ-{bot} (bot): {q_bot}, out Q (bot): {_min}')
    if isinstance(Series, pd.core.series.Series):
        return Series[(out_top|out_bot)].index
    else:
        return Series[(out_top|out_bot)]
    

def idb(
    data:pd.core.frame.DataFrame,
    k:int=1000,
    rn:bool=False,
    table:str=f'##tmp_{time.strftime("%jd")}',
    v:int=0,
    noret:bool=False,
    repl:bool=False
) -> (None, list):
    '''
    if noret = False then return list 
    if noret = True then print str 
    -------
    k: rows in batch;
    rn: if true then upload with index (range 1 to n);
    table: table name in database;
    v: verbose
    noret = False (if True then will be returned None object and batches will be printed)
    repl: if True then respaces
    -------
    example:
      idb(df, noret=True, v=1)
    ===
      idb(df, k=4, noret=False, v=1)
    ===
      # for silence:
        res = idb(pd.read_clipboard(), k=100, rn=True, v=0, noret=False)
        # print(res[-1])
        with engine.connect() as conn:
            for i in range(len(res)):    
                conn.execute(res[i])
                
    # if need another engine use create_engine from sqlalchemy: 
    #     _engine = create_engine(str(engine.url).replace('_MAIN_22', '_MAIN_23'))'''
    df = data.copy(deep=True)
    if k > df.shape[0]:
        k = df.shape[0]
    command = 'INSERT INTO {} VALUES '.format(table)
    if rn:
        df.reset_index(inplace=True)
        df['index'] = df.index + 1
    df['_#concat'] = (
        df[df.columns[0]].astype('string').fillna('')
        .str.cat(
            others=df[df.columns[1:]].astype('string').fillna(''),
            sep="','"
        ).str.replace('^.*\S+', lambda m: f"('{m.group(0)}')", regex=True)
    )
    ins=list()
    if v==1:
        print(f"parts: {-(-df.shape[0] // k)}")
    if repl:
        for i in range(1, (-(-df.shape[0] // k) + 1)):
            if v==1:
                print(f'#{i}: {(i-1)*k}--{(i-1)*k+k-1 if (i-1)*k+k-1 < df.shape[0] else df.shape[0]}')
            ins.append(
                '''{}{}'''.format(
                    command,
                    df.loc[(i-1)*k : (i-1)*k+k-1, '_#concat']
                    .replace(to_replace ='\s+', value = ' ',regex=True)
                    .str.cat(sep=',')
                )
            )
            if v==1 and not noret:
                print(ins[-1],'\n==============')
    else:
        for i in range(1, (-(-df.shape[0] // k) + 1)):
            if v==1:
                print(f'#{i}: {(i-1)*k}--{(i-1)*k+k-1 if (i-1)*k+k-1 < df.shape[0] else df.shape[0]}')
            ins.append(
                '''{}{}'''.format(
                    command,
                    df.loc[(i-1)*k : (i-1)*k+k-1, '_#concat']
                    .str.cat(sep=',')
                )
            )
            if v==1 and not noret:
                print(ins[-1],'\n==============')
    if noret:
        print('***\n',*ins,sep='\n')
        return
    if v == 1:
        print('\n****')
        print(*ins,sep='\n')
    return ins


def xlconvert(
    writer:pd.io.excel._openpyxl.OpenpyxlWriter,
    num:bool=False,
    dates:(bool, str)=True,
    time:bool=True,
    head:bool=False)-> None:
    '''
    call it for convert columns in Excel-file
    --------
    num: if Ture then append whitespace between numbers (for visual design)
    dates: 
        if True then convert dates in date-format ->  YYYY-MM-DD 
        if False then convert dates in text-format ->  YYYY-MM-DD 
        can be pattern (string)
    time: 
        if True then setting time format (if exists) -> date-format + time(h:mm:ss.ms)
        ! if False and  dates == False  then delete time-value in cell
    head: if True then convert header cells in text-format
    
    --------
    example:
    
    filename = 'example.xlsx'
    with pd.ExcelWriter('try.xlsx') as w:
        data.to_excel(w, sheet_name = 's1')
        xlconvert(w, dates='d.mm', time=True, head=True, num=True)
    #     xlconvert(w, dates=True, time=False, head=True) # correct design date-dtype (in excel)
    #     xlconvert(w, dates=False)
        
    '''
    try:
        assert isinstance(writer.book.worksheets, list)
    except Exception as err:
        return err
    
    if isinstance(dates, str):
        date_format = dates
    else: 
        if not time:
            date_format = r'yyyy\-mm\-dd;@'
        else:
            date_format = r'yyyy\-mm\-dd'

    if num:
        inum = r'#,##0_);(#,##0)'
        fnum = r'#,##0.00_);(#,##0.00)'
    else:
        inum = r'0'
        fnum = r'0,00'
        
    func = lambda x : max(map(int, x.strftime('%T%f').split(':')))
    
    for sheet in range(0, len(writer.book.worksheets)):
        ws = writer.book.worksheets[sheet]
        last_row = ws.max_row
        last_col = ws.max_column
        head_row = 0
        min_check_row = list()

        for i in range(1, last_row):
            if not ws.cell(i, last_col).has_style:
                head_row = i - 1
                break

        if head and head_row:
            for col in range(1, last_col + 1):
                for row in range(1, head_row + 1):
                    ws.cell(row, col).number_format = '@'

        for col in range(1, last_col + 1):
            for check_row in range(head_row + 1, last_row + 1):
                if ws.cell(check_row, col).value != None and ws.cell(check_row, col).value != '':
                    checktype = ws.cell(check_row, col).value
                    min_check_row.append(check_row)
                    break

            if last_row-head_row-check_row + 1 <= 0:
                continue

            if isinstance(checktype, pd.Timestamp):
                if not func(ws.cell(check_row, col).value) or not time:
                    if not dates:
                        for row in range(check_row, last_row + 1):
                            ws.cell(row, col).number_format = date_format
                            ws.cell(row, col).value = str(ws.cell(row, col).value.date())
                            ws.cell(row, col).number_format = '@'
                    else:
                        for row in range(check_row, last_row + 1):
                            ws.cell(row, col).number_format = date_format

                else:
                    if not dates:
                        for row in range(check_row, last_row + 1):
                            ws.cell(row, col).number_format = date_format + r' h:mm:ss.000'
                            ws.cell(row, col).value = str(ws.cell(row, col).value)
                            ws.cell(row, col).number_format = '@'
                    else:
                        for row in range(check_row, last_row + 1):
                            ws.cell(row, col).number_format = date_format + r' h:mm:ss.000'
                        
            elif isinstance(checktype, (bool, str)):
                for row in range(check_row, last_row + 1):
                    ws.cell(row, col).number_format = '@'       
            elif isinstance(checktype, int):
                for row in range(check_row, last_row + 1):
                    ws.cell(row, col).number_format = inum
            elif isinstance(checktype, float):
                for row in range(check_row, last_row + 1):
                    ws.cell(row, col).number_format = fnum

        if min(min_check_row) - head_row - 1:
            ws.delete_rows(head_row + 1)
    return


pd.set_option('display.max_columns', 0) 
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', 0)
pd.set_option('display.max_rows', 111)
pd.set_option('display.min_rows', 0)

print('''{a}\n{b}
\nimport pyspark.pandas as ps
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[2]').appName('envI').getOrCreate()
sparkdf = spark.read.parquet(sel('parquet')[0])
\nimport matplotlib.pyplot as plt
import seaborn as sns
\n{c}\n{d}'''.format(
    a=': '.join(['version', sys.version]),
    b=': '.join(['platfrom', sys.platform]),
    c=realtime(),
    d=os.getcwd()
))
