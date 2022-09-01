df = 
    usecols=['Humantestid', 'Participantfk', 'Region_ht', 'Subjectcode',
             'Processcondition', 'Primarymarkc', 'Testresultc',
             'Towntypefk', 'Testtypecode'])

s_time = time.time()
pf = df.iloc[
    df[
        (df.Processcondition == 6) & (df.Testtypecode == 4)
    ].Testresultc.dropna().apply(lambda x: len(x)).sort_values().index.tolist()
].copy(deep=True)
# pf[~pf.Region.isin(pf.Region_ht)]

pf['c'] = pf.Testresultc.apply(lambda x: [i for i in x[0::4]])
pf['maxc'] = pf.Testresultc.apply(lambda x: [i for i in x[2::4]])

qf = pf.explode(['c', 'maxc']).copy(deep=True)
qf['tasknumber'] = qf.groupby('Humantestid').cumcount() + 1

cols = ['Region_ht', 'Towntypefk', 'Subjectcode', 'tasknumber', 'maxc', 'Humantestid', 'c']
ff = qf[cols].groupby(cols[0:-2]).agg({
    'Humantestid': lambda x: x.nunique(),
    'maxc': lambda x: x.astype(np.int64).sum(),
    'c': lambda x: x.astype(np.int64).sum()}).copy(deep=True)

print(time.time() - s_time)
ff.head(23)
# plt.figure(figsize=(25,15))
# sns.lineplot(data=ff[ff.index.get_level_values(1) == 3], hue='Towntypefk', x='tasknumber', y='c')