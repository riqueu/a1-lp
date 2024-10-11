import pandas as pd
import numpy as np
import seaborn as sns
from data_cleaner import *

clean_paralympic_atletes_dataset()

def count_athletes(df, *args):
    df = df.groupby(list(args))['Medal'].count().unstack(fill_value=0)
    df['Total_Athletes'] = df.sum(axis=1)
    df = df.reset_index()
    df.rename(columns={'F': 'F_Athletes', 'M': 'M_Athletes'}, inplace=True)
    return df

def update_medals_or_score(df, medal_or_score, *args, **kwargs):
    if medal_or_score == 'Medal':
        df = df.groupby(list(args))['Medal'].apply(lambda x:  (x != 0).sum()).unstack(fill_value=0).reset_index()
    else:
        df = df.groupby(list(args))['Medal'].apply(lambda x: x.sum()).unstack(fill_value=0).reset_index()
        
    df.rename(columns=kwargs, inplace=True)
    df[f'Total_{medal_or_score}'] = df[[f'F_{medal_or_score}', f'M_{medal_or_score}']].sum(axis=1)
    
    
    return df

def merge_by_country(df_main, df_aux):
    df_main = pd.merge(
        df_main,
        df_aux,
        how='outer',
        on=['Year', 'NOC']
    )
    
    return df_main

def merge_by_year(df_main, df_aux):
    df_main = pd.merge(
        df_main,
        df_aux,
        how='outer',
        on='Year'
    )
    
    return df_main

df1 = pd.read_csv("data/athlete_events.csv")
df2 = pd.read_csv("data/modified_medal_athlete.csv")
df3 = pd.read_csv("data/summer_paralympics.csv")
df4 = pd.read_csv("data/winter_paralympics.csv")
df3 = pd.concat([df3, df4])
df3.sort_values(by=['Year'], inplace=True)
df1 = medals_to_int(df1)


# Analise 1: Participacao e rendimento dos atletas do brasil comparado com o mundo (agrupado por ano)
# Separado em paises por ano
df_olymp_countries = df1.drop_duplicates(['Year', 'Name'])
df_olymp_countries = count_athletes(df_olymp_countries, *['Year', 'NOC','Sex'])

df_paralymp_countries = df3[['Year', 'Country_Code', 'Women', 'Men', 'P_Total']]
df_paralymp_countries = df_paralymp_countries.rename(columns={'Country_Code': 'NOC', 'Women': 'F_Athletes', 'Men': 'M_Athletes', 'P_Total': 'Total_Athletes'})

# Todos os paises agrupados por ano
df_olymp = df1.drop_duplicates(['Year', 'Name'])
df_olymp = count_athletes(df_olymp, *['Year', 'Sex']) 

df_paralymp = df3.groupby(['Year'])[['Men', 'Women', 'P_Total']].sum()
df_paralymp.rename(columns={'Women': 'F_Athletes', 'Men': 'M_Athletes', 'P_Total': 'Total_Athletes'}, inplace=True)

# Conta a quantidade de medalhas separada pelo genero do atleta e agrupada por ano
# Quantidade de medalhas por país por ano
df_aux = update_medals_or_score(df1, 'Medal', *['Year', 'NOC', 'Sex'], **{'F': 'F_Medal', 'M': 'M_Medal'})
df_olymp_countries = merge_by_country(df_olymp_countries, df_aux)

df_aux = update_medals_or_score(df2, 'Medal', *['Games_year', 'Npc_new', 'Sex'], **{'Games_year': 'Year','Npc_new': 'NOC', 'F': 'F_Medal', 'M': 'M_Medal'})
df_paralymp_countries = merge_by_country(df_paralymp_countries, df_aux)
df_paralymp_countries.dropna(inplace=True)

df_aux = update_medals_or_score(df1, 'Medal', *['Year', 'Sex'], **{'F': 'F_Medal', 'M': 'M_Medal'})
df_olymp = merge_by_year(df_olymp, df_aux)

df_aux = update_medals_or_score(df2, 'Medal', *['Games_year', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Medal', 'M': 'M_Medal'})
df_paralymp = merge_by_year(df_paralymp, df_aux)
df_paralymp.dropna(inplace=True)

# Pontuacao do pais por ano (baseado no peso das medalhas)
df_aux = update_medals_or_score(df1, 'Score', *['Year', 'NOC', 'Sex'], **{'F': 'F_Score', 'M': 'M_Score'})
df_olymp_countries = merge_by_country(df_olymp_countries, df_aux)
df_olymp_countries[df_olymp_countries.columns.difference(['NOC'])] = df_olymp_countries[df_olymp_countries.columns.difference(['NOC'])].astype(int)

df_aux = update_medals_or_score(df2, 'Score', *['Games_year', 'Npc_new', 'Sex'], **{'Games_year': 'Year','Npc_new': 'NOC', 'F': 'F_Score', 'M': 'M_Score'})
df_paralymp_countries = merge_by_country(df_paralymp_countries, df_aux)
df_paralymp_countries.dropna(inplace=True)
df_paralymp_countries[df_paralymp_countries.columns.difference(['NOC'])] = df_paralymp_countries[df_paralymp_countries.columns.difference(['NOC'])].astype(int)

df_aux = update_medals_or_score(df1, 'Score', *['Year', 'Sex'], **{'F': 'F_Score', 'M': 'M_Score'})
df_olymp = merge_by_year(df_olymp, df_aux).astype(int)

df_aux = update_medals_or_score(df2, 'Score', *['Games_year', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Score', 'M': 'M_Score'})
df_paralymp = merge_by_year(df_paralymp, df_aux)

df_paralymp.dropna(inplace=True)
df_paralymp = df_paralymp.astype('int64')

# Analise 2: Participacao e rendimento dos atletas do brasil comparado com o mundo (agrupado por esporte)