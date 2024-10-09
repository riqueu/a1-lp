import numpy as np
import pandas as pd
from data_cleaner import transform_athletes_df_to_paralympics_format


# Upload dos DataFrames
athletes_df = pd.read_csv("../data/athlete_events.csv")
summer_paralympics_df = pd.read_csv("../data/summer_paralympics.csv")
winter_paralympics_df = pd.read_csv("../data/winter_paralympics.csv")
noc_df = pd.read_csv("../data/noc_regions.csv").rename(columns={'region': 'Country'})
gdp_df = pd.read_csv("../data/gdp/gdp.csv").drop(columns=['Code', 'Unnamed: 65'])


def merge_noc_with_country(df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Faz merge do DataFrame de entrada com noc_regions_df para adicionar a coluna 'Country' com base no 'NOC' e reordenar as colunas conforme especificado.

    Args:
        df (pd.DataFrame): O DataFrame a ser processado.
        noc_regions_df (pd.DataFrame): O DataFrame que contém as informações de NOC e País.

    Returns:
        pd.DataFrame: O DataFrame mesclado e reordenado.
    """
    # Faz merge do DataFrame passado com noc_regions_df para adicionar (ou atualizar) a coluna 'Country'
    df = df.merge(noc_df[['NOC', 'Country']], on='NOC', how='left')
    
    return df[['Year', 'Country', 'NOC', 'Season', 'Gold', 'Silver', 'Bronze', 'M_Total', 'Men', 'Women', 'P_Total']]


def transform_gdp_data(gdp_df: pd.DataFrame) -> pd.DataFrame:
    # Transforma o DataFrame de PIB de formato wide para formato long
    gdp_df = gdp_df.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP')
    
    # Converte a coluna 'Year' para tipo numérico (int)
    gdp_df['Year'] = gdp_df['Year'].astype(int)
    
    # Renomeia a coluna 'Country Name' para 'Country' para facilitar os merges posteriores
    gdp_df = gdp_df.rename(columns={'Country Name': 'Country'})
    
    gdp_df = gdp_df[['Year', 'Country', 'GDP']]

    gdp_df = gdp_df.sort_values(by=['Year', 'Country'])

    return gdp_df


def prepare_olympics_paralympics_pib_analysis(athletes_df: pd.DataFrame, summer_paralympics_df: pd.DataFrame, winter_paralympics_df: pd.DataFrame, gdp_df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    # Limpa e transforma o DataFrame das Olimpíadas
    olympics_df = transform_athletes_df_to_paralympics_format(athletes_df)

    summer_paralympics_df.drop(columns=['Host_City', 'Host_Country', 'Country'], inplace=True)
    summer_paralympics_df['Season'] = 'Summer'

    winter_paralympics_df.drop(columns=['Host_City', 'Host_Country', 'Country'], inplace=True)
    winter_paralympics_df['Season'] = 'Winter'

    # Concatena as Paralimpíadas de verão e inverno
    paralympics_df = pd.concat([summer_paralympics_df, winter_paralympics_df], ignore_index=True)

    paralympics_df = paralympics_df.rename(columns={'Country_Code': 'NOC'})

    # Crie uma coluna 'Country' com base nas colunas 'NOC' no olympics_df e no paralympics_df
    clean_olympics_df = merge_noc_with_country(olympics_df, noc_df).sort_values(by=['Year', 'Country'])
    clean_paralympics_df = merge_noc_with_country(paralympics_df, noc_df)

    clean_olympics_df['Event'] = 'Olympics'
    clean_paralympics_df['Event'] = 'Paralympics'

    sports_df = pd.concat([clean_olympics_df, clean_paralympics_df], ignore_index=True)

    gdp_df = transform_gdp_data(gdp_df)

    combined_df = pd.merge(sports_df, gdp_df, on=['Year', 'Country'], how='left')
    
    return combined_df


# Aplica as funções, limpando e organizando os dois DataFrames para que possamos iniciar a análise
# olympics_df = transform_olympics_to_paralympics_format(olympics_df) 
# paralympics_df = merge_noc_with_country(paralympics_df, noc_regions_df)

prepare_olympics_paralympics_pib_analysis(athletes_df, summer_paralympics_df, winter_paralympics_df, gdp_df, noc_df)

# print(prepare_olympics_paralympics_pib_analysis(athletes_df, summer_paralympics_df, winter_paralympics_df, gdp_df, noc_df))
# print(transform_gdp_data(gdp_df))

# TODO: Rever a ordem do combined_df, pois ele está agrupando por Events

# TODO: Ver em quantas linhas o GDP é NaN, e com base nisso, excluí-las ou tomar outra atitude

# TODO: Verificar se o combined_df está correto e pode ser usado para a análise