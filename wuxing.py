def makekart(y:int, m:int, d:int, *h, todf:bool=False, verbose:bool=False)->list:
    h = h[0] if h else None
    karta = list()
    n = list(range(1,6))
    z = list(range(1,13))
    lst = [[n[(i - 1) // 2 % 5], z[(i - 1) % 12]] for i in range(1,61)]

    G = lst[y % 60 - 4]
    zv = lst[lst.index(G) % 5 * 10 + lst.index(G) % 5 * 2:
        lst.index(G) % 5 * 10 + lst.index(G) % 5 * 2 + 14]
    M = (zv[m - 1]
        if (d < 4 and m == 2)
        or (d < 5 and m == 4)
        or (d < 6 and m in (1, 3, 5, 6))
        or (d < 7 and m in (7, 11, 12))
        or (d < 8 and m in (8, 9, 10))
        else zv[m])

    y_c, y_n, m_n = 0, 0, 0
    if (y % 4 == 0 and y % 100 != 0) or not y % 400:
        if m < 3:
            m_n = int((m + 1) % 2 * 30 + round((0.6 * (m + 13) - 3) - 6))
        if m == 3:
            m_n = round((m + 1) % 2 * 30 + (0.6 * (m + 1) - 3))
        if m > 3:
            m_n = int((m + 1) % 2 * 30 + (0.6 * (m + 1) - 3))
    else: 
        if m < 3:
            m_n = int((1 + m) % 2 * 30 + round((0.6 * (m + 13) -3 ) - 5))
        if m == 3:
            m_n = round((m + 1) % 2 * 30 + (0.6 * (m + 1) - 3))
        if m > 3:
            m_n = int((m + 1) % 2 * 30 + (0.6 * (m + 1) - 3))

    y_c = y // 400 - y // 100 + 10
    y_n = (y % 400 % 80  % 12 * 5 + y % 400  % 80  // 4) % 60
    k = (y_n + y_c + m_n + d) % 60 - 1

    if h is None:
        karta.append(None)
    else:
        time = lst[k % 5 * 10 + 2 * (k % 5):k % 5 * 10 + 2 * (k % 5) + 13]
        for i in range(0, 25, 2):
            if i-1 <= h < i + 1:
                karta.append([time[i // 2][0] if not time.index(time[i // 2]) % 2 else -(time[i // 2][0]), time[i // 2][1]])
    
    karta.append([lst[k][0] if not k % 2 else -(lst[k][0]), lst[k][1]])
    karta.append([M[0] if not lst.index(M) % 2 else -(M[0]), M[1]])
    karta.append([G[0] if not lst.index(G) % 2 else -(G[0]), G[1]] if M not in zv[0:2]
                  else [lst[lst.index(G) - 1] if not (lst.index(G) - 1) % 2 else [-(lst[lst.index(G) - 1][0]), lst[lst.index(G) - 1][1]]])

    if verbose:
        elements = dict(zip(n, ['дерево', 'огонь', 'земля', 'металл', 'вода']))
        bsts = dict(zip(z, ['крыса', 'бык', 'тигр', 'кролик', 'дракон', 'змея', 'лошадь', 'коза', 'обезьяна', 'петух', 'собака', 'свинья']))
        print(*zip(['-'.join(['yan' if l[0] > 0 else 'in', elements[abs(l[0])]]) for l in karta if l],
                   [bsts[l[1]] for l in karta if l]))
    return karta


def stars(kart:list, describe:bool=False)->list:
    def descr(starlist:list, elems:int)->list:
        elements = dict(zip(list(range(1,6)), ['дерево', 'огонь', 'земля', 'металл', 'вода'])) 
        bsts = dict(zip(list(range(1,13)),
                        ['крыса', 'бык', 'тигр', 'кролик', 'дракон', 'змея', 'лошадь', 'коза',
                         'обезьяна', 'петух', 'собака', 'свинья']))
        flag = False
        func = lambda x, e=True: '-'.join(['инь' if x<0 else 'ян', elements[abs(x)]]) if e else bsts[x]
        if elems == 1:
            return list(map(' | '.join, list(map(lambda x: [func(x[0]), func(x[1], flag)], starlist))))
        elif elems == 2:
            return list(map(' | '.join, list(map(lambda x: [func(x[0], flag), func(x[1])], starlist))))
        else:
            return list(map(' | '.join, list(map(lambda x: [func(x[0], flag), func(x[1], flag)], starlist))))
    
    def add(c:int, name:str):
        baz[c].append(name)
        if describe and name not in lst.keys():
            lst[name] = descr(star, elems)
        return
    
    forzip = [['час'], ['день'], ['месяц'], ['год']]
    polar = list(i.copy() for i in forzip)
    dd, dy = kart[1][0], kart[3][0]
    day, year = kart[1][1], kart[3][1]
    seq = range(1 if not kart[0] else 0, 4)
    pol = ['братство', 'грабитель богатства', 'дух пищи', 'дух мятежа', 
           'косое богатство', 'прямое богатство', 'косая власть', 'прямая власть',
           'косая печать', 'прямая печать']
 
    func = lambda x: list(pol[i * 2:i * 2 + 2][dd * x[0] < 0] for i in range(5)
                      if abs(x[0]) - 1 == (abs(dd) - 1 + i) % 5)
    for c in seq:
        if c != 1:
            polar[c].append(*func(kart[c]))
    
    baz = list(i.copy() for i in forzip)
    baz.append(['glob'])
    
    ground_sky_func = lambda x: any(kart[x][1] == i[1] for i in star if kart[x][0] == i[0])
    ground_func = lambda x, y: any(kart[x][1] == i[1] for i in star if i[0] == y)
    dd_dy_func = lambda x: any(kart[x][1] == i[1] for i in star if i[0] in (dd, dy))  
    day_year_func = lambda x: any(kart[x][1] == i[1] and i[0] == day and x != 1
                          or kart[x][1] == i[1] and i[0] == year and x != 3
                          for i in star if i[0] in (day, year))
    
    lst = dict() if describe else None
    elems = False
    rng = list(range(4,13,4)) + list(range(3,12,4)) + list(range(2,11,4)) + list(range(1,10,4))
    jiv = list(); list(map(lambda x: jiv.extend([x]*3), (1,4,7,10)))
    star = list(zip(rng, jiv))
    [add(c, 'цветок персика') for c in seq if day_year_func(c)]

    rng = list(range(1,10,4))+list(range(2,11,4))+list(range(3,12,4))+list(range(4,13,4))
    jiv = list(); list(map(lambda x: jiv.extend([x]*3), (3, 12, 9, 6)))
    star = list(zip(rng, jiv))
    [add(c, 'почтовая лошадь') for c in seq if day_year_func(c)]

    jiv = list(); list(map(lambda x: jiv.extend([x]*3), (1, 10, 7, 4)))
    star = list(zip(rng, jiv))
    [add(c, 'звезда генерала') for c in seq if day_year_func(c)]

    jiv = list(); list(map(lambda x: jiv.extend([x]*3), (5, 2, 11, 8)))
    star = list(zip(rng, jiv))
    [add(c, 'звезда искусств') for c in seq if day_year_func(c)]

    jiv = list(); list(map(lambda x: jiv.extend([x]*3), (12, 9, 6, 3)))
    star = list(zip(rng, jiv))
    [add(c, 'звезда бедствий') for c in seq if day_year_func(c)]

    rng = list(i % 12 if i != 12 else i % 13 for i in range(3,15))
    jiv = list(); list(map(lambda x: jiv.extend([x]*3), [2,5,8,11]))
    star = list(zip(rng,jiv))
    [add(c, 'звезда одиночества (ж)') for c in seq if day_year_func(c)]

    jiv = list(); list(map(lambda x: jiv.extend([x]*3), [6, 9, 12, 3]))
    star = list(zip(rng, jiv))
    [add(c, 'звезда одиночества (м)') for c in seq if day_year_func(c)]

    rng = list(range(1, 13))
    jiv = list(i % 12 + 1 for i in range(15, 3, -1))
    star = list(zip(rng,jiv))
    [add(c, 'красный луань') for c in seq if c != 1 and ground_func(c, day)]
    
    rng = list(range(1,13))
    jiv = list(i%12 if i !=12 else i % 13 for i in range(8,20))
    star = list(zip(rng, jiv))
    [add(c, 'исходное созвезие (м+ / ж-)') for c in seq if ground_func(c, year)]
    
    jiv = [i%12 if i != 12 else i%13 for i in range(6,18)]
    star = list(zip(rng, jiv))
    [add(c, 'исходное созвезие (м- / ж+)') for c in seq if ground_func(c, year)]

    jiv = [5, 2, 11, 8] * 3
    star = list(zip(rng, jiv))
    [add(c, 'цветущий балдахин') for c in seq if day_year_func(c)]

    ## no lst      
    rng = [(0,6), (4, 0), (-2,0),  (0,9), (5, 0), (-4,0),  (0,12), (1, 0), (-5,0),  (0,3), (2, 0), (-1,0)] 
    jiv = list(range(1,13))
    star = list(zip(rng, jiv))
    func = lambda x: any(i[0][0] == kart[x][0] or i[0][1] == kart[x][1] for i in star if kart[2][1] == i[1])
    [baz[c].append('небесная добродетель') for c in seq if func(c)]
#     [add(c, 'небесная добродетель') for c in seq if func(c)]    ##

    elems = 1
    rng = list(); list(map(lambda x: rng.extend([x, x, -x, -x]), range(1,6)))
    jiv = [2,8,1,9,10,12,10,12,2,8,1,9,2,8,3,7,4,6,4,6]
    star= list(zip(rng, jiv))
    [add(c, 'благородный') for c in seq if dd_dy_func(c)]
    
    jiv = [1,7, 2,6, 3,5, 10,12, 1,7, 2,6, 1,7, 8,12, 9,11, 4,6]
    star= list(zip(rng, jiv))
    [add(1, 'благородный 6ти союзов') for i in star if i[0] == dd and i[1] == day]
    
    jiv = [4,0,3,5,7,0,6,8,7,0,6,8,10,0,9,11,1,0,2,12]
    star = list(filter(lambda x: x[1] != 0, zip(rng, jiv)))
    [add(c, 'овечий нож') for c in seq if ground_func(c, dd)]
    
    rng = list(); list(map(lambda x: rng.extend([x, -x]), range(1,6)))
    jiv = [3, 4, 6, 7, 6, 7, 9, 10, 12, 1]
    star = list(zip(rng, jiv))
    [add(c, '10 небесных стволов') for c in seq if ground_func(c, dd)]
    
    jiv = list(i % 12 if i < 11 else (i - 3) % 13 for i in range(6, 21) if i not in (8, 11, 14, 16, 18)) 
    star = list(zip(rng, jiv))
    [add(c, 'звезда академика') for c in seq if dd_dy_func(c)]
    
    jiv = [7, 7, 3, 8, 5, 5, 11, 10, 1, 9]
    star = list(zip(rng,jiv))
    [add(c, 'ша цветущего персика') for c in seq if ground_func(c, dd)]
    
    jiv = [5, 6, 8, 9, 8, 9, 11, 12, 2, 3]
    star = list(zip(rng, jiv))
    [add(c, 'золотая карета') for c in seq if ground_func(c, dd)]
    
    jiv = [5, 6, 9, 12, 11, 2, 5, 6, 9, 12]
    star = list(zip(rng,jiv))
    [add(c, 'звезда банкротства') for c in seq if ground_sky_func(c)]
    
    rng = [3, 4, 4, 5]
    jiv = [11, 5, 11, 5]
    star = list(zip(rng, jiv))
    [add(c, 'куйганг') for c in seq if ground_sky_func(c)]
    
    rng = [2, -2, 3, -4, 5, -5, 2, -2, 3, -4, 5, -5]
    jiv = list(range(1, 13))
    star = list(zip(rng, jiv))
    [add(c, 'ошибка инь-ян') for c in seq if ground_sky_func(c)]
    
    rng = [1, -1, 2, -2, 3, 3, -4, 5]
    jiv = [5, 6, 7, 6, 9, 7, 12, 1]
    star = list(zip(rng,jiv))
    [add(c, 'одинокий феникс') for c in seq if ground_sky_func(c)]
    
    rng = [1, 1, 1, 1, 2, 3, 4, 5]
    jiv = [2, 5, 8, 11] * 2
    star = list(zip(rng,jiv))
    [add(c, 'денежное хранилище') for c in seq if ground_func(c, abs(dd))]

    func = lambda x: (
        (5 in list(i[1] for i in x[-1::-2]) and 6 in list(i[1] for i in x[-2::-1])) 
        or (6 in list(i[1] for i in x[-1::-2]) and 5 in list(i[1] for i in x[-2::-1])))
    if func(kart):
        baz[-1].append('сеть земли')
    
    func = lambda x: (
        (11 in list(i[1] for i in x[-1::-2]) and 12 in list(i[1] for i in x[-2::-1]))
        or (12 in list(i[1] for i in x[-1::-2]) and 11 in list(i[1] for i in x[-2::-1])))
    if func(kart):
        baz[-1].append('сеть небес')
        
    rng = list(range(1,6))
    jiv = [4, 7, 7, 10, 1]
    star = list(zip(rng,jiv))
    if ground_func(2, dd):
        add(-1, 'янский край')
    if describe:
        return polar, baz, lst
    else:
        return polar, baz
    
    
def checkbz(y:int, m:int, d:int, h:int=None):
    if all([isinstance(i, int) for i in [y,m,d]]):
        s = list(map(int, [y,m,d]))
    if h and 23 < int(h):
        raise ValueError(f'hour must be < 23(:59:59) (NOT {h})')
    elif not h:
            h = None
    s.append(h)
    if not 1 <= m <= 12:
        raise ValueError(f'month must be between 1 and 12 (NOT {m})')
    mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        mes[1] = mes[1] + 1
    if mes[int(m)-1]%int(d) >= mes[int(m)-1]:
        raise ValueError(f'{m} month dont have {d}`s day')
    return s

    
def bzdf(y,m,d, *h, todf:bool=False):
    dates = checkbz(y, m, d, *h)
    kart = makekart(*dates)
    star = stars(kart)
    elements = dict(zip(list(range(1,6)), ['дерево', 'огонь', 'земля', 'металл', 'вода'])) 
    bsts = dict(zip(list(range(1,13)),
                    ['крыса', 'бык', 'тигр', 'кролик', 'дракон', 'змея', 'лошадь', 'коза',
                     'обезьяна', 'петух', 'собака', 'свинья']))
    func = lambda x: '-'.join(['инь' if x<0 else 'ян', elements[abs(x)]]) if x else '-'
    if not todf:
        dates.reverse()
        cols = list(map(lambda x: x[0], star[1]))
        [star[0].append(['-'] * (len(cols) - len(star[0])))]
        [star[0][i].extend('-') for i in range(len(cols)) if len(star[0][i]) < 2]
        [print(
            '\t|'.join([
                str(dates[i]) if i < 4 and dates[i] != None else '*',
                ': '.join(
                    [cols[i],
                     ' '.join([
                         '-' if not kart[i] else func(kart[i][0]),
                         '' if not kart[i] else bsts[kart[i][1]]
                     ]) if i < 4 else '']
                ), star[0][i][1]]),
            ', '.join(star[1][i][1:]),
            sep='\n\t' if star[1][i][1:] else '',
        ) for i in range(len(cols))]
        return
    else:
        import numpy as np
        import pandas as pd
        
        
        cols = np.array(
            ['date'] 
            + list(map(lambda x: x[0], star[1]))
            + ['polarity', 'p_hour', 'p_day', 'p_month', 'p_year'])  
    df = pd.DataFrame(star[1]).T.iloc[1:,:].reset_index(drop=True)
    df = pd.concat([
        pd.Series(np.nan),
        df,
        pd.Series(star[0])[pd.Series(star[0]).str.len() > 1].str.join(': ').reset_index(drop=True)
    ], axis=1, ignore_index=True)
    
    lst = list(' '.join([
        '' if not kart[i] else func(kart[i][0]),
        '' if not kart[i] else bsts[kart[i][1]]]) for i in range(4))
    df['p_hour'] = np.nan if not h else lst[0]
    df['p_day'] = lst[1]
    df['p_month'] = lst[2]
    df['p_year'] = lst[3]
    df[0] = pd.Timestamp(year = dates[0], month = dates[1], day = dates[2], hour = dates[-1])
    df.columns = cols
    df.rename(columns={'год':'s_year','месяц':'s_month','день':'s_day','час':'s_hour'}, inplace=True)
    df = df.replace({None:np.nan}).convert_dtypes()

    return df

# bzdf(2018, 7, 26, todf=True)
