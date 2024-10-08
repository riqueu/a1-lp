import pandas as pd
import numpy as np
import seaborn as sns
from data_cleaner import *


df = pd.read_csv("data/athlete_events.csv")
df = medals_to_int(df)

# Filtra o dataframe para pegar apenas os atletas do Brasil
bra_df = df[df['NOC']=='BRA']

# Primeira analise: Quantidade de medalhas gerais dos atletas de todos os paises por ano e Quantidade de medalhas de atletas femininas de todos os paises por ano
# Soma a quantidade de medalhas de atletas de todos os paises agrupada por ano
medals_year = df.groupby(['Year', 'Sex'])['Medal'].apply(lambda x: (x != 0).sum()).unstack(fill_value=0)
medals_year['Total'] = medals_year.sum(axis=1)
print(medals_year.head())


# Soma a quantidade de medalhas de atletas do brasil agrupada por ano
medals_bra_year = bra_df.groupby(['Year', 'Sex'])['Medal'].apply(lambda x: (x != 0).sum()).unstack(fill_value=0)
medals_bra_year['Total'] = medals_bra_year.sum(axis=1)
print(medals_bra_year.head())

