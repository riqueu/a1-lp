import pandas as pd
from data_cleaner import *

import unittest


class TestMedalsToInt(unittest.TestCase):
    
    #  Ts
    
    pass



if __name__== "__main__":
    unittest.main()
df = pd.read_csv('data/athlete_events.csv')
df = df[['Name', 'Sex', 'Age', 'Weight', 'Height', 'Sport']]
# df= df.head(10000)
# df_t = df[['Sport', 'Sex', 'Age']].groupby(['Sport', 'Sex']).count()
# poucos_dados = df_t[df_t['Age'] == 1].reset_index()['Sport']
# df = df[~df['Sport'].isin(poucos_dados)]
# df_1 = predict_missing(df)
# print(df_1)
df_bktb = df[df['Sport']=="Basketball"]
df_bktb = df_bktb[['Name', 'Sex', 'Age', 'Weight', 'Height', 'Sport']]


print(len(df_bktb))
df_tratado = predict_missing(df_bktb)
print(df_tratado)
print(len(df_tratado))

print(len(df))

df_tratado = predict_missing(df)
print(df_tratado)
print(len(df_tratado))
# df_tratado= predict_missing(df)
# print(len(df_tratado))

