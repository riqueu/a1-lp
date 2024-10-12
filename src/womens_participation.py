"""Módulo com funções para análise e visualização de participação e rendimento dos atletas do Brasil comparado com o mundo."""

import pandas as pd
import numpy as np
import seaborn as sns
from data_cleaner import *


def count_athletes(df: pd.DataFrame, *args) -> pd.DataFrame:
    """Função que conta a quantidade de atletas por país e por ano.

    Args:
        df (pd.DataFrame): df dos atletas

    Returns:
        pd.DataFrame: df com a quantidade de atletas por país e por ano
    """
    df = df.groupby(list(args))['Medal'].count().unstack(fill_value=0)
    df['Total_Athletes'] = df.sum(axis=1)
    df = df.reset_index()
    df.rename(columns={'F': 'F_Athletes', 'M': 'M_Athletes'}, inplace=True)
    
    return df


def update_medals_or_score(df: pd.DataFrame, medal_or_score: str, *args, **kwargs) -> pd.DataFrame:
    """Função que atualiza o df com a quantidade de medalhas ou pontuação por país e por ano.

    Args:
        df (pd.DataFrame): df dos atletas
        medal_or_score (str): Indicando o que deve ser atualizado

    Returns:
        pd.DataFrame: _description_
    """
    if medal_or_score == 'Medal':
        df = df.groupby(list(args))['Medal'].apply(lambda x:  (x != 0).sum()).unstack(fill_value=0).reset_index()
    else:
        df = df.groupby(list(args))['Medal'].apply(lambda x: x.sum()).unstack(fill_value=0).reset_index()
        
    df.rename(columns=kwargs, inplace=True)
    df[f'Total_{medal_or_score}'] = df[[f'F_{medal_or_score}', f'M_{medal_or_score}']].sum(axis=1)
    
    return df


def merge_by_country(df_main: pd.DataFrame, df_aux: pd.DataFrame) -> pd.DataFrame:
    """Função que faz merge de dois dataframes por país e por ano.

    Args:
        df_main (pd.DataFrame): dataframe principal
        df_aux (pd.DataFrame): dataframe auxiliar

    Returns:
        pd.DataFrame: dataframe com os dois dataframes mergeados
    """
    df_main = pd.merge(
        df_main,
        df_aux,
        how='outer',
        on=['Year', 'NOC']
    )
    
    return df_main


def merge_by_year(df_main: pd.DataFrame, df_aux: pd.DataFrame) -> pd.DataFrame:
    """Função que faz merge de dois dataframes por ano.

    Args:
        df_main (pd.DataFrame): dataframe principal
        df_aux (pd.DataFrame): dataframe auxiliar

    Returns:
        pd.DataFrame: dataframe com os dois dataframes mergeados
    """
    df_main = pd.merge(
        df_main,
        df_aux,
        how='outer',
        on='Year'
    )
    
    return df_main

def merge_by_sport(df_main: pd.DataFrame, df_aux: pd.DataFrame) -> pd.DataFrame:
    """Função que faz merge de dois dataframes por esporte e por ano.

    Args:
        df_main (pd.DataFrame): dataframe principal
        df_aux (pd.DataFrame): dataframe auxiliar

    Returns:
        pd.DataFrame: dataframe com os dois dataframes mergeados
    """
    df_main = pd.merge(
        df_main,
        df_aux,
        how='outer',
        on=['Year', 'Sport']
    )
    
    return df_main


def create_dataframes() -> tuple:
    """Função que cria os dataframes para a análise e visualização de participação e rendimento dos atletas do Brasil comparado com o mundo.

    Returns:
        tuple: dataframes para análise
    """
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
    df2_olymp = df1.drop_duplicates(['Year','Sport', 'Name'])
    df2_olymp = count_athletes(df2_olymp, *['Year', 'Sport','Sex'])

    df2_paralymp = df2.drop_duplicates(['Games_year','Sport', 'Athlete_name'])
    df2_paralymp = count_athletes(df2_paralymp, *['Games_year','Sport', 'Sex'])
    df2_paralymp.rename(columns={'Games_year': 'Year'}, inplace=True)

    # Olimpiada e Paralimpiada por esporte no Brasil
    df2_olymp_bra = df1[df1['NOC'] == 'BRA']
    df2_olymp_bra = df2_olymp_bra.drop_duplicates(['Year','Sport', 'Name'])
    df2_olymp_bra = count_athletes(df2_olymp_bra, *['Year', 'Sport','Sex']) 

    df2_paralymp_bra = df2[df2['Npc_new'] == 'BRA']
    df2_paralymp_bra = df2_paralymp_bra.drop_duplicates(['Games_year','Sport', 'Athlete_name'])
    df2_paralymp_bra = count_athletes(df2_paralymp_bra, *['Games_year','Sport', 'Sex']) 
    df2_paralymp_bra.rename(columns={'Games_year': 'Year'}, inplace=True)

    # Quantidade de medalhas por esporte e por ano
    df_aux = update_medals_or_score(df1, 'Medal', *['Year', 'Sport', 'Sex'], **{'F': 'F_Medal', 'M': 'M_Medal'})
    df2_olymp = merge_by_sport(df2_olymp, df_aux)

    df_aux = update_medals_or_score(df2, 'Medal', *['Games_year', 'Sport', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Medal', 'M': 'M_Medal'})
    df2_paralymp = merge_by_sport(df2_paralymp, df_aux)
    df2_paralymp.dropna(inplace=True)

    df_aux = update_medals_or_score(df1[df1['NOC'] == 'BRA'], 'Medal', *['Year', 'Sport', 'Sex'], **{'F': 'F_Medal', 'M': 'M_Medal'})
    df2_olymp_bra = merge_by_sport(df2_olymp_bra, df_aux)

    df_aux = update_medals_or_score(df2[df2['Npc_new'] == 'BRA'], 'Medal', *['Games_year', 'Sport', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Medal', 'M': 'M_Medal'})
    df2_paralymp_bra = merge_by_sport(df2_paralymp_bra, df_aux)

    # Pontuacao do pais por esporte (baseado no peso das medalhas)
    df_aux = update_medals_or_score(df1, 'Score', *['Year', 'Sport', 'Sex'], **{'F': 'F_Score', 'M': 'M_Score'})
    df2_olymp = merge_by_sport(df2_olymp, df_aux)
    df2_olymp[df2_olymp.columns.difference(['Sport'])] = df2_olymp[df2_olymp.columns.difference(['Sport'])].astype(int)

    df_aux = update_medals_or_score(df2, 'Score', *['Games_year', 'Sport', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Score', 'M': 'M_Score'})
    df2_paralymp = merge_by_sport(df2_paralymp, df_aux)
    df2_paralymp[df2_paralymp.columns.difference(['Sport'])] = df2_paralymp[df2_paralymp.columns.difference(['Sport'])].astype(int)

    df_aux = update_medals_or_score(df1[df1['NOC'] == 'BRA'], 'Score', *['Year', 'Sport', 'Sex'], **{'F': 'F_Score', 'M': 'M_Score'})
    df2_olymp_bra = merge_by_sport(df2_olymp_bra, df_aux)
    df2_olymp_bra[df2_olymp_bra.columns.difference(['Sport'])] = df2_olymp_bra[df2_olymp_bra.columns.difference(['Sport'])].astype(int)

    df_aux = update_medals_or_score(df2[df2['Npc_new'] == 'BRA'], 'Score', *['Games_year', 'Sport', 'Sex'], **{'Games_year': 'Year', 'F': 'F_Score', 'M': 'M_Score'})
    df2_paralymp_bra = merge_by_sport(df2_paralymp_bra, df_aux)
    df2_paralymp_bra[df2_paralymp_bra.columns.difference(['Sport'])] = df2_paralymp_bra[df2_paralymp_bra.columns.difference(['Sport'])].astype(int)

    return df_olymp, df_olymp_countries, df_paralymp, df_paralymp_countries, df2_olymp, df2_olymp_bra, df2_paralymp, df2_paralymp_bra

def estimate_statistics(df):
    df_with_outliers = df[['F_Athletes', 'F_Medal', 'F_Score']].describe()    
    df = df[(df['F_Athletes'] > 0) & (df['F_Medal'] > 0) & (df['F_Score'] > 0)]
    df_without_outliers = df[['F_Athletes', 'F_Medal', 'F_Score']].describe()
    
    return pd.concat([df_with_outliers, df_without_outliers])
