import pandas as pd
import numpy as np
from math import isnan
df1 = pd.DataFrame({'A1' : [np.nan, 'foo', 'bar', 'spam', np.nan],'A2' : ['1', np.nan, '3', '5', np.nan], 'B' : [np.nan, '2', '3', np.nan, '6']})
print(df1)
df2 = pd.DataFrame({'A' : ['5', '2', '4', None, '3', '7'],'B' : [None, None, '3', '4', '6', '8'],'C' : ['1','2', '3.', '4.', '6.', '8.']})
print(df2)
a = df1.join(df2, rsuffix='_r')
print(a)
b = list(set(df1.columns) & set(df2.columns))
print(b)
c = a.loc[:,b[0]].isnull()
print(c)
d = [x+'_r' for x in b]
print(d)
a.loc[c,b[0]] = a.loc[c,d[0]]
a.drop(d[0],axis=1,inplace=True)
print(a)
z = dict(a.loc[0])
print(z)

z['A1'] == z['A1']
z['B'] == z['B']

isnan(z['A1'])
isnan(z['B'])