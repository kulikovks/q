## created 25.11.2020
def day(y, m, d, h):
    y, m, d, h = int(y), int(m), int(d), h
    result = list()
    lst=list()
    n = ['дерево', 'огонь', 'земля', 'металл', 'вода']
    z = ['крыса', 'бык', 'тигр', 'кролик', 'дракон', 'змея', 'лошадь', 'коза', 'обезьяна', 'петух', 'собака', 'свинья']
    for i in range(0, 60):
        lst.append([n[(i//2)%5] +' '+ z[i%12]])    

    G = lst[(int(y)%60)-4]
    zv = lst[int((str(lst.index(G)%5))+str((lst.index(G)%5)*2)):(int(
        (str(lst.index(G)%5))+str((lst.index(G)%5)*2))+14)]
    if (d<6 and int(m) in (1,3,5,6)) or (d<7 and int(m) in (7,11,12)) or (
            d<8 and int(m) in (8,9,10)) or (d<4 and int(m) == 2) or (
                d<5 and int(m) == 4): 
        M = zv[int(m)-1]
    else:
        M = zv[int(m)]
 
    y_c, y_n, m_n = 0, 0, 0
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        if m < 3:
            m_n = int(((1+m)%2)*30 + round((0.6 * (m+13) -3)-6))
        if m == 3:
            m_n = round(((m+1)%2)*30 + (0.6 * (m+1) - 3))
        if m > 3:
            m_n = int(((m+1)%2)*30 + (0.6 * (m+1) - 3))
    else: 
        if m < 3:
            m_n = int(((1+m)%2)*30 + round((0.6 * (m+13) -3)-5))
        if m == 3:
            m_n = round(((m+1)%2)*30 + (0.6 * (m+1) - 3))
        if m > 3:
            m_n = int(((m+1)%2)*30 + (0.6 * (m+1) - 3))

    y_c = ((y//400)-(y//100))+10
    y_n = ((((y%400)%80)%12)*5 +(((y%400)%80)//4))%60
    k = ((y_n+y_c+m_n+d)%60)-1
    
    result.append(['yan']+lst[k] if k%2==0 else ['in']+lst[k])    
    result.append(['yan']+M if lst.index(M)%2==0 else ['in']+M)
    if M in zv[0:2]:
        result.append(['yan']+lst[lst.index(G)-1] if (
            lst.index(G)-1)%2==0 else ['in']+lst[lst.index(G)-1])
    if M not in zv[0:2]:
        result.append(['yan']+G if lst.index(G)%2==0 else ['in']+G)

    time =[]
    if k%5==0:
        time = lst[0:13]
    if k%5==1:
        time = lst[12:25]
    if k%5==2:
        time = lst[24:37]
    if k%5==3:
        time = lst[36:49]
    if k%5==4:
        time = lst[48::]+[lst[0]]
        
    if h == '' or not isinstance(h, int):
        result.append(['','',''])
        #[time[i] for i in range(13)]
    else:
        if 0 <= h < 1:
            result.append(['yan']+time[0])
        elif 1 <= h < 3:
            result.append(['in']+time[1])
        if 3 <= h < 5:
            result.append(['yan']+time[2])
        if 5 <= h < 7:
            result.append(['in']+time[3])
        if 7 <= h < 9:
            result.append(['yan']+time[4])
        if 9 <= h < 11:
            result.append(['in']+time[5])
        if 11 <= h < 13:
            result.append(['yan']+time[6])
        if 13 <= h < 15:
            result.append(['in']+time[7])
        if 15 <= h < 17:
            result.append(['yan']+time[8])
        if 17 <= h < 19:
            result.append(['in']+time[9])
        if 19 <= h < 21:
            result.append(['yan']+time[10])
        if 21 <= h < 23:
            result.append(['in']+time[11])
        if 23 <= h <= 24:
            result.append(['yan']+time[12])    
    result[0],result[1],result[-2],result[-1]=result[-1],result[0],result[1],result[-2]
    return result


def bz(day_list):
    z = ['крыса', 'бык', 'тигр', 'кролик', 'дракон', 
         'змея', 'лошадь', 'коза', 'обезьяна', 'петух',
         'собака', 'свинья']

    lst = []
    if len(day_list[0]) > 2:
        for i in range(len(day_list)):
            if i == 0:
                lst.append(['9999', '9999'])
            else:    
                lst.append(day_list[i].copy())
    else:
        for i in range(len(day_list)):
            lst.append(day_list[i].copy())

    p = 1 if len(lst[0][0]) not in (1,2,3) else 0     
    for i in range(len(lst)):
        if p == 1 and i == 3:
            break
        if len(lst[p+i][0]) == 3:
            lst[p+i][0]='+'
        if len(lst[p+i][0]) == 2:
            lst[p+i][0]='-'
        if 'дерево' in lst[p+i][1]:
            lst[p+i][1]=lst[p+i][1].replace('дерево', '0')
        if 'огонь' in lst[p+i][1]:
            lst[p+i][1]=lst[p+i][1].replace('огонь', '1')
        if 'земля' in lst[p+i][1]:
            lst[p+i][1]=lst[p+i][1].replace('земля', '2')
        if 'металл' in lst[p+i][1]:
            lst[p+i][1]=lst[p+i][1].replace('металл', '3')
        if 'вода' in lst[p+i][1]:
            lst[p+i][1]=lst[p+i][1].replace('вода', '4')            
    dd = lst[1][0]+lst[1][1]
  
    baz = []
    p = 1 if len(lst[0][0]) not in (1,2,3) else 0
    
    for j in range(len(lst)):
        if p == 1 and j == 3:
            break 
        if int(dd[1]) == int(lst[p+j][1][0]):
            if lst[p+j][0] == dd[0]:
                baz.append(["братство"])
            elif lst[p+j][0] != dd[0]:
                baz.append(["грабитель богатства"])
        elif int(dd[1]) == (int(lst[p+j][1][0])+4)%5:
            if lst[p+j][0] == dd[0]:
                baz.append(["дух наслаждения"])
            elif lst[p+j][0] != dd[0]:
                baz.append(["дух мятежа"])      
        elif int(dd[1]) == (int(lst[p+j][1][0])+3)%5:
            if lst[p+j][0] == dd[0]:
                baz.append(["косое богатство"])
            elif lst[p+j][0] != dd[0]:
                baz.append(["прямое богатство"])   
        elif int(dd[1]) == (int(lst[p+j][1][0])+2)%5:
            if lst[p+j][0] == dd[0]:
                baz.append(["косая власть"])
            elif lst[p+j][0] != dd[0]:
                baz.append(["прямая власть"])
        elif int(dd[1]) == (int(lst[p+j][1][0])+1)%5:
            if lst[p+j][0] == dd[0]:
                baz.append(["косая печать"])
            elif lst[p+j][0] != dd[0]:
                baz.append(["прямая печать"])
                
    if p == 1:
        del baz[0]    
    elif p == 0:
        del baz[1]

    klmn = []
    for k in range(4):
        if (((z.index(lst[1][1][2:]) in (0,4,8) and k !=1) or (z.index(lst[3][1][2:]) in (0,4,8) and k != 3)) and lst[k][1][2:].count(z[9]) > 0)or (
                ((z.index(lst[1][1][2:]) in (3,7,11) and k !=1) or (z.index(lst[3][1][2:]) in (3,7,11) and k != 3)) and lst[k][1][2:].count(z[0]) > 0) or (
                    ((z.index(lst[1][1][2:]) in (2,6,10) and k !=1) or (z.index(lst[3][1][2:]) in (2,6,10) and k != 3)) and lst[k][1][2:].count(z[3]) > 0) or (
                        ((z.index(lst[1][1][2:]) in (1,5,9) and k !=1) or (z.index(lst[3][1][2:]) in (1,5,9) and k != 3)) and lst[k][1][2:].count(z[6]) > 0):
            klmn.append([k, 'цветок персика'])
        if (((z.index(lst[1][1][2:]) in (0,4,8) and k !=1) or (z.index(lst[3][1][2:]) in (0,4,8) and k != 3)) and lst[k][1][2:].count(z[2]) > 0)or (
                ((z.index(lst[1][1][2:]) in (3,7,11) and k !=1) or (z.index(lst[3][1][2:]) in (3,7,11) and k != 3)) and lst[k][1][2:].count(z[5]) > 0) or (
                    ((z.index(lst[1][1][2:]) in (2,6,10) and k !=1) or (z.index(lst[3][1][2:]) in (2,6,10) and k != 3)) and lst[k][1][2:].count(z[8]) > 0) or (
                        ((z.index(lst[1][1][2:]) in (1,5,9) and k !=1) or (z.index(lst[3][1][2:]) in (1,5,9) and k != 3)) and lst[k][1][2:].count(z[11]) > 0):
            klmn.append([k, 'почтовая лошадь'])
        if (((z.index(lst[1][1][2:]) in (0,4,8) and k !=1) or (z.index(lst[3][1][2:]) in (0,4,8) and k != 3)) and lst[k][1][2:].count(z[0]) > 0)or (
                ((z.index(lst[1][1][2:]) in (3,7,11) and k !=1) or (z.index(lst[3][1][2:]) in (3,7,11) and k != 3)) and lst[k][1][2:].count(z[3]) > 0) or (
                    ((z.index(lst[1][1][2:]) in (2,6,10) and k !=1) or (z.index(lst[3][1][2:]) in (2,6,10) and k != 3)) and lst[k][1][2:].count(z[6]) > 0) or (
                        ((z.index(lst[1][1][2:]) in (1,5,9) and k !=1) or (z.index(lst[3][1][2:]) in (1,5,9) and k != 3)) and lst[k][1][2:].count(z[9]) > 0):
            klmn.append([k, 'звезда генерала'])
        if (((z.index(lst[1][1][2:]) in (0,4,8) and k !=1) or (z.index(lst[3][1][2:]) in (0,4,8) and k != 3)) and lst[k][1][2:].count(z[4]) > 0)or (
                ((z.index(lst[1][1][2:]) in (3,7,11) and k !=1) or (z.index(lst[3][1][2:]) in (3,7,11) and k != 3)) and lst[k][1][2:].count(z[7]) > 0) or (
                    ((z.index(lst[1][1][2:]) in (2,6,10) and k !=1) or (z.index(lst[3][1][2:]) in (2,6,10) and k != 3)) and lst[k][1][2:].count(z[10]) > 0) or (
                        ((z.index(lst[1][1][2:]) in (1,5,9) and k !=1) or (z.index(lst[3][1][2:]) in (1,5,9) and k != 3)) and lst[k][1][2:].count(z[1]) > 0):
            klmn.append([k, 'звезда искусств'])
        if (((z.index(lst[1][1][2:]) in (0,4,8) and k !=1) or (z.index(lst[3][1][2:]) in (0,4,8) and k != 3)) and lst[k][1][2:].count(z[11]) > 0)or (
                ((z.index(lst[1][1][2:]) in (3,7,11) and k !=1) or (z.index(lst[3][1][2:]) in (3,7,11) and k != 3)) and lst[k][1][2:].count(z[2]) > 0) or (
                    ((z.index(lst[1][1][2:]) in (2,6,10) and k !=1) or (z.index(lst[3][1][2:]) in (2,6,10) and k != 3)) and lst[k][1][2:].count(z[5]) > 0) or (
                        ((z.index(lst[1][1][2:]) in (1,5,9) and k !=1) or (z.index(lst[3][1][2:]) in (1,5,9) and k != 3)) and lst[k][1][2:].count(z[8]) > 0):
            klmn.append([k, 'звезда бедствий'])

    for k in range(4):
            if (z.index(lst[3][1][2:]) == (0) and k !=3 and lst[k][1][2:].count(z[3]) > 0) or (
                   z.index(lst[3][1][2:]) == (3) and k !=3 and lst[k][1][2:].count(z[0]) > 0) or (
                       z.index(lst[3][1][2:]) == (1) and k !=3 and lst[k][1][2:].count(z[2]) > 0) or (
                           z.index(
                lst[3][1][2:]) == (2) and k !=3 and lst[k][1][2:].count(z[1]) > 0) or (
                    z.index(lst[3][1][2:]) == (4) and k !=3 and lst[k][1][2:].count(z[11]) > 0) or (
                        z.index(lst[3][1][2:]) == (11) and k !=3 and lst[k][1][2:].count(z[4]) > 0) or (
                            z.index(
                lst[3][1][2:]) == (5) and k !=3 and lst[k][1][2:].count(z[10]) > 0) or (
                    z.index(lst[3][1][2:]) == (10) and k !=3 and lst[k][1][2:].count(z[5]) > 0) or (
                        z.index(lst[3][1][2:]) == (6) and k !=3 and lst[k][1][2:].count(z[9]) > 0) or (
                            z.index(
                lst[3][1][2:]) == (9) and k !=3 and lst[k][1][2:].count(z[6]) > 0) or (
                    z.index(lst[3][1][2:]) == (7) and k !=3 and lst[k][1][2:].count(z[8]) > 0) or (
                        z.index(lst[3][1][2:]) == (8) and k !=3 and lst[k][1][2:].count(z[7]) > 0):
                    klmn.append([k, 'красный луань'])
                    
    for i in range(12):
        if z.index(z[i]) == (z.index(lst[3][1][2:]) + 7)%12:
            for c in range(4):
                if z[i] in lst[c][1]:
                    klmn.append([c, 'исходное созвездие М(ян)/Ж(инь)'])
        if z.index(z[i]) == (z.index(lst[3][1][2:]) + 5)%12:
            for c in range(4):
                if z[i] in lst[c][1]:
                    klmn.append([c, 'исходное созвездие М(инь)/Ж(ян)'])
    if z[i] in ((z[(z.index(lst[3][1][2:])+3)%12]),(
            z[(z.index(lst[3][1][2:])+2)%12]),(
                z[(z.index(lst[3][1][2:])+1)%12])):
        for c in range(4):
            if z[i] in lst[c][1] and c != 3:
                klmn.append([c, 'приют одиночества (для М)'])
    if z[i] in (z[1], z[4], z[7], z[10]):
        for c in range(4):
            if z[i] in lst[c][1] and c != 3:
                klmn.append([c, 'приют одиночества (для Ж)'])
                
    seti = 0
    lovushka = 0
    seti1 = 0
    lovushka1 = 0           
    for j in range(4):
        if (((int(dd[1]) == 0 and dd[0] == '-') or (int(dd[1]) == 2 and dd[0] == '-')) and (z[8] in lst[j][1] or z[0] in lst[j][1])) or (
            ((int(dd[1]) == 0 and dd[0] == '+') or (int(dd[1]) == 2 and dd[0] == '+') or (int(dd[1]) == 3 and dd[0] == '+')) and (z[1] in lst[j][1] or z[7] in lst[j][1])) or (
                (int(dd[1]) == 1) and (z[11] in lst[j][1] or z[9] in lst[j][1])) or (
                    (int(dd[1]) == 3 and dd[0] == '-') and (z[2] in lst[j][1] or z[6] in lst[j][1])) or (
                        (int(dd[1]) == 4) and (z[3] in lst[j][1] or z[5] in lst[j][1])):
            klmn.append([j, "благородный"])
        if (((int(dd[1]) == 0 and dd[0] == '+') and (z[2] in lst[j][1])) or (
            (int(dd[1]) == 0 and dd[0] == '-') and (z[3] in lst[j][1])) or (
                (int(dd[1]) in (1, 2) and dd[0] == '+') and (z[5] in lst[j][1])) or (
                    (int(dd[1]) in (1, 2) and dd[0] == '-') and (z[6] in lst[j][1])) or (
                        (int(dd[1]) == 3 and dd[0] == '+') and (z[8] in lst[j][1])) or(
                            (int(dd[1]) == 3 and dd[0] == '-') and (z[9] in lst[j][1])) or(
                                (int(dd[1]) == 4 and dd[0] == '+') and (z[11] in lst[j][1])) or(
                                    (int(dd[1]) == 4 and dd[0] == '-') and (z[0] in lst[j][1]))):
            klmn.append([j, "10 небесных стволов"])
        if (((int(dd[1]) == 0 and dd[0] == '+') and (z[5] in lst[j][1])) or (
            (int(dd[1]) == 0 and dd[0] == '-') and (z[6] in lst[j][1])) or (
                (int(dd[1]) in (1, 2) and dd[0] == '+') and (z[8] in lst[j][1])) or (
                    (int(dd[1]) in (1, 2) and dd[0] == '-') and (z[9] in lst[j][1])) or (
                        (int(dd[1]) == 3 and dd[0] == '+') and (z[11] in lst[j][1])) or(
                            (int(dd[1]) == 3 and dd[0] == '-') and (z[0] in lst[j][1])) or(
                                (int(dd[1]) == 4 and dd[0] == '+') and (z[2] in lst[j][1])) or(
                                    (int(dd[1]) == 4 and dd[0] == '-') and (z[3] in lst[j][1]))):
            klmn.append([j, "звезда академика"])
        if (((int(dd[1]) == 0 and dd[0] == '+') and (z[3] in lst[j][1])) or (
            (int(dd[1]) == 0 and dd[0] == '-') and (z[4] in lst[j][1] or z[2] in lst[j][1])) or (
                (int(dd[1]) in (1, 2) and dd[0] == '+') and (z[6] in lst[j][1])) or (
                    (int(dd[1]) in (1, 2) and dd[0] == '-') and (z[5] in lst[j][1] or z[7] in lst[j][1])) or (
                        (int(dd[1]) == 3 and dd[0] == '+') and (z[9] in lst[j][1])) or(
                            (int(dd[1]) == 3 and dd[0] == '-') and (z[8] in lst[j][1] or z[10] in lst[j][1])) or(
                                (int(dd[1]) == 4 and dd[0] == '+') and (z[0] in lst[j][1])) or(
                                    (int(dd[1]) == 4 and dd[0] == '-') and (z[1] in lst[j][1]  or z[11] in lst[j][1]))):
            klmn.append([j, "овечий нож"])
        if (((int(dd[1]) == 0 and dd[0] in '+-') and (z[6] in lst[j][1])) or (
            (int(dd[1]) == 1 and dd[0] == '+') and (z[2] in lst[j][1])) or (
                (int(dd[1]) == 1 and dd[0] == '-') and (z[7] in lst[j][1])) or (
                    (int(dd[1]) == 2 and dd[0] in '+-') and (z[4] in lst[j][1])) or (
                        (int(dd[1]) == 3 and dd[0] == '+') and (z[10] in lst[j][1])) or(
                            (int(dd[1]) == 3 and dd[0] == '-') and (z[9] in lst[j][1])) or(
                                (int(dd[1]) == 4 and dd[0] == '+') and (z[0] in lst[j][1])) or(
                                    (int(dd[1]) == 4 and dd[0] == '-') and (z[8] in lst[j][1]))):
            klmn.append([j, "ша цветущего персика"])
        if (((int(dd[1]) == 0 and dd[0] in '+') and (z[9] in lst[j][1])) or (
                (int(dd[1]) == 0 and dd[0] == '-') and (z[8] in lst[j][1])) or (
                    (int(dd[1]) == 1 and dd[0] == '+') and (z[0] in lst[j][1])) or (
                        (int(dd[1]) == 1 and dd[0] in '-') and (z[11] in lst[j][1])) or (
                            (int(dd[1]) == 2 and dd[0] == '+') and (z[3] in lst[j][1])) or(
                                (int(dd[1]) == 2 and dd[0] == '-') and (z[2] in lst[j][1])) or(
                                    (int(dd[1]) == 3 and dd[0] == '+') and (z[6] in lst[j][1])) or(
                                        (int(dd[1]) == 3 and dd[0] == '-') and (z[5] in lst[j][1])) or(
                                            (int(dd[1]) == 4 and dd[0] == '+') and (z[1] in lst[j][1] or z[7] in lst[j][1])) or(
                                                (int(dd[1]) == 4 and dd[0] == '-') and (z[4] in lst[j][1] or z[10] in lst[j][1]))):
            klmn.append([j, "небесная добродетель"])
        if (((int(dd[1]) == 0 and dd[0] in '+') and (z[4] in lst[j][1])) or (
                (int(dd[1]) == 0 and dd[0] == '-') and (z[5] in lst[j][1])) or (
                    (int(dd[1]) == 1 and dd[0] == '+') and (z[7] in lst[j][1])) or (
                        (int(dd[1]) == 1 and dd[0] in '-') and (z[8] in lst[j][1])) or (
                            (int(dd[1]) == 2 and dd[0] == '+') and (z[7] in lst[j][1])) or(
                                (int(dd[1]) == 2 and dd[0] == '-') and (z[8] in lst[j][1])) or(
                                    (int(dd[1]) == 3 and dd[0] == '+') and (z[10] in lst[j][1])) or(
                                        (int(dd[1]) == 3 and dd[0] == '-') and (z[11] in lst[j][1])) or(
                                            (int(dd[1]) == 4 and dd[0] == '+') and (z[1] in lst[j][1])) or(
                                                (int(dd[1]) == 4 and dd[0] == '-') and (z[2] in lst[j][1]))):
             klmn.append([j, "золотая карета"])
        if (((int(lst[j][1][0]) == 3 and lst[j][0] in '+') and (z[4] in lst[j][1] or z[10] in lst[j][1])) or(
                (int(lst[j][1][0]) == 4 and lst[j][0] in '+') and (z[4] in lst[j][1])) or (
                    (int(lst[j][1][0]) == 2 and lst[j][0] in '+') and (z[10] in lst[j][1]))):
             klmn.append([j, "куйганг"])
        if (((int(lst[j][1][0]) == 1 and lst[j][0] in '+') and (z[0] in lst[j][1] or z[6] in lst[j][1])) or (
                (int(lst[j][1][0]) == 1 and lst[j][0] in '-') and (z[1] in lst[j][1] or z[7] in lst[j][1])) or (
                    (int(lst[j][1][0]) == 2 and lst[j][0] in '+') and (z[2] in lst[j][1] or z[8] in lst[j][1])) or (
                        (int(lst[j][1][0]) == 3 and lst[j][0] in '-') and (z[3] in lst[j][1] or z[9] in lst[j][1])) or (
                            (int(lst[j][1][0]) == 4 and lst[j][0] in '+') and (z[4] in lst[j][1] or z[10] in lst[j][1])) or(
                                (int(lst[j][1][0]) == 4 and lst[j][0] in '-') and (z[5] in lst[j][1] or z[11] in lst[j][1]))):
            klmn.append([j, "ошибка инь-ян"])
        if (((int(lst[j][1][0]) == 0 and lst[j][0] in '+') and (z[4] in lst[j][1])) or (
                (int(lst[j][1][0]) in (0,1) and lst[j][0] in '-') and (z[5] in lst[j][1])) or (
                    (int(lst[j][1][0]) == 3 and lst[j][0] in '-') and (z[11] in lst[j][1])) or (
                        (int(lst[j][1][0]) == 2 and lst[j][0] in '+') and (z[8] in lst[j][1] or z[6] in lst[j][1])) or (
                            (int(lst[j][1][0]) == 4 and lst[j][0] in '+') and (z[2] in lst[j][1] or z[0] in lst[j][1])) or(
                                (int(lst[j][1][0]) == 1 and lst[j][0] in '+') and (z[6] in lst[j][1]))):
            klmn.append([j, "одинокий феникс"])
        if (((int(lst[j][1][0]) in (0,3) and lst[j][0] in '+') and (z[4] in lst[j][1])) or (
                (int(lst[j][1][0]) in (0,3) and lst[j][0] in '-') and (z[5] in lst[j][1])) or (
                    (int(lst[j][1][0]) in (1,4) and lst[j][0] in '+') and (z[8] in lst[j][1])) or (
                        (int(lst[j][1][0]) in (1,4) and lst[j][0] in '-') and (z[11] in lst[j][1])) or (
                            (int(lst[j][1][0]) == 2 and lst[j][0] in '+') and (z[10] in lst[j][1])) or(
                                (int(lst[j][1][0]) == 2 and lst[j][0] in '-') and (z[1] in lst[j][1]))):
            klmn.append([j, "звезда банкротства"])
            
        if lst[j][1].count(z[10]):
            seti += 1
        if lst[j][1].count(z[4]):
            lovushka +=1
        if lst[j][1].count(z[11]):
            seti1 += 1
        if lst[j][1].count(z[5]):
            lovushka1 += 1            
    if seti != 0 and seti1 != 0:
        klmn.append([7,"сети небес"])
    if lovushka != 0 and lovushka1 != 0:
        klmn.append([7,"ловушка земли"])
    klmn.sort()
    
    for i in range (len(klmn)):
        if klmn[i][0] == 0:
            klmn[i][0] = 'час'
        if klmn[i][0] == 1:
            klmn[i][0] = 'день'
        if klmn[i][0] == 2:
            klmn[i][0] = 'месяц'
        if klmn[i][0] == 3:
            klmn[i][0] = 'год'
        if klmn[i][0] == 7:
            del klmn[i][0]
    if 'час' not in [i[0] for i in klmn]:
        klmn.insert(0, ['час', None])
    return ([baz]+[klmn])

## update
def lbztodf(s, f, g):
    import numpy as np
    import pandas as pd
    
    maps = ['-'.join(i) if any(i) else np.nan for i in f]
    stars = pd.DataFrame(g[1]).pivot(columns=0, values=1)
    L = max(len(g[0]), max([stars.loc[:,i].dropna().shape[0] for i in stars.columns]))
    c = []
    for i in [stars.loc[:,i].dropna().tolist() for i in stars.columns]:
        while L > len(i):
            i.append(np.nan)
        c.append(i)
    stars = pd.DataFrame.from_dict(dict(zip(stars.columns.tolist(), c)))
    
    if 'день' not in stars.columns:
        stars['день'] = np.nan
    elif 'месяц' not in stars.columns:
        stars['месяц'] = np.nan
    elif 'час' not in stars.columns:
        stars['час'] = np.nan
    elif 'год' not in stars.columns:
        stars['год'] = np.nan
    
    tag = ['час','месяц','год']
    stars['polarity'] = [*map(': '.join, zip(tag[3-len(g[0]):], [i[0] for i in g[0]]))] + ([np.nan]*(stars.shape[0] - len(g[0])))
    stars['p_year'] = [maps[-1]] * (stars.shape[0])
    stars['p_month'] = [maps[-2]] * (stars.shape[0])
    stars['p_day'] = [maps[-3]] * (stars.shape[0])
    stars['p_hour'] = [maps[-4]] * (stars.shape[0])
    stars['date'] = pd.Timestamp(year = s[0], month = s[1], day = s[2], hour = s[-1])
    stars = stars.rename(columns={'год':'s_year','день':'s_day','месяц':'s_month','час':'s_hour'})[['date', 's_hour', 's_day', 's_month', 's_year', 'polarity', 'p_hour', 'p_day', 'p_month', 'p_year']].convert_dtypes()
    return stars

def checkbz(y:int, m:int, d:int, *h:int):
    if all([isinstance(i, int) for i in [y,m,d]]):
        s = [*map(int, [y,m,d])]
    if not h or not(isinstance(h[0], int) or h[0].isdigit()):
        h=''
    elif 23 < int(h[0]):
        raise ValueError(f'hour must be < 24  (NOT {h[0]})')
    else:
        h = abs(h[0])
    s.append(h)
    if 1 > m  or m > 12:
        raise ValueError(f'month must be between 1 and 12 (NOT {m})')
    mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0:
        mes[1] = mes[1] + 1
    if mes[int(m)-1]%int(d) >= mes[int(m)-1]:
        raise ValueError(f'{m} month dont have {d}`s day')
    return lbztodf(s, day(*s), bz(day(*s)))

def bzdf(df:bool=True, *s):
    if s:
        return checkbz(*s)
    else:
        y, m, d, h = int(input('year: ')), int(input('month: ')), int(input('day: ')), input('hour(:00==:59): ')
        h = int(h) if h.isdigit() else ''
        if not df:
            s = [y, m, d, h]
            f = day(*s)
            g = bz(f)
            print(*s,*f,*g, sep='\n')
            return s
        else:
            return checkbz(y,m,d,h)
# bzdf(df=False)
