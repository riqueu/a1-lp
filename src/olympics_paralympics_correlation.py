import numpy as np
import pandas as pd


# Upload dos DataFrames
olympics_df = pd.read_csv("../data/athlete_events.csv")
summer_paralympics_df = pd.read_csv("../data/summer_paralympics.csv").drop(columns=['Host_City', 'Host_Country', 'Country'])
winter_paralympics_df = pd.read_csv("../data/winter_paralympics.csv").drop(columns=['Host_City', 'Host_Country', 'Country'])
noc_regions_df = pd.read_csv("../data/noc_regions.csv").rename(columns={'region': 'Country'})

# Adiciona a coluna 'Season', que será importante para podermos concatenar os DataFrames
summer_paralympics_df['Season'] = 'Summer'
winter_paralympics_df['Season'] = 'Winter'

# Concatena os dois DataFrames de paralimpíadas
paralympics_df = pd.concat([summer_paralympics_df, winter_paralympics_df], ignore_index=True)
paralympics_df = paralympics_df.rename(columns={'Country_Code': 'NOC'})

wanted_columns_order = ['Year', 'Country', 'NOC', 'Season', 'Gold', 'Silver', 'Bronze', 'M_Total', 'Men', 'Women', 'P_Total']


def merge_noc_with_country(df: pd.DataFrame, noc_regions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Faz merge do DataFrame de entrada com noc_regions_df para adicionar a coluna 'Country' com base no 'NOC' e reordenar as colunas conforme especificado.

    Args:
        df (pd.DataFrame): O DataFrame a ser processado.
        noc_regions_df (pd.DataFrame): O DataFrame que contém as informações de NOC e País.

    Returns:
        pd.DataFrame: O DataFrame mesclado e reordenado.
    """
    # Faz merge do DataFrame passado com noc_regions_df para adicionar (ou atualizar) a coluna 'Country'
    df = df.merge(noc_regions_df[['NOC', 'Country']], on='NOC', how='left')
    
    return df[wanted_columns_order]


def transform_olympics_to_paralympics_format(olympics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma o DataFrame de atletas olímpicos no formato utilizado pelos DataFrames paralímpicos

    Args:
        olympics_df (pd.DataFrame): DataFrame contendo os dados dos atletas olímpicos com as colunas:

    Returns:
        pd.DataFrame: Um DataFrame formatado como os DataFrames paralímpicos
    """
    olympics_df = olympics_df[olympics_df['Year'] >= 1960]

    grouped_df = olympics_df.groupby(['NOC', 'Year', 'Season']).agg(
        Gold=('Medal', lambda x: (x == 'Gold').sum()),
        Silver=('Medal', lambda x: (x == 'Silver').sum()),
        Bronze=('Medal', lambda x: (x == 'Bronze').sum()),
        Men=('Sex', lambda x: (x == 'M').sum()),
        Women=('Sex', lambda x: (x == 'F').sum())
    ).reset_index()

    # Calcula os totais e os atribui para suas respectivas novas colunas
    grouped_df['M_Total'] = grouped_df['Gold'] + grouped_df['Silver'] + grouped_df['Bronze']
    grouped_df['P_Total'] = grouped_df['Men'] + grouped_df['Women']

    grouped_df = merge_noc_with_country(grouped_df, noc_regions_df)
    grouped_df = grouped_df.sort_values(by=['Year', 'Country'])

    return grouped_df


# Aplica as funções, limpando e organizando os dois DataFrames para que possamos iniciar a análise
olympics_df = transform_olympics_to_paralympics_format(olympics_df) 
paralympics_df = merge_noc_with_country(paralympics_df, noc_regions_df)

