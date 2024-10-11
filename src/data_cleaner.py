"""Módulo com funções para limpeza de dados."""

import pandas as pd
import numpy as np
import doctest


def validade_athletes_columns(df: pd.DataFrame) -> None:
    """A função que confere se possui todas as colunas necessárias para análise

    Args:
        df (pd.DataFrame): dataframe
        
        Index:
            RangeIndex
        Columns:
            Name: 'ID' - int64
            Name: 'Name' - object
            Name: 'Sex' - object
            Name: 'Age' - float64
            Name: 'Height' - float64
            Name: 'Weight' - float64
            Name: 'Team' - object
            Name: 'NOC' - object
            Name: 'Games' - object
            Name: 'Year' - int64
            Name: 'Season' - object
            Name: 'City' - object
            Name: 'Sport' - object
            Name: 'Event' - object
            Name: 'Medal' - object
        
    Returns:
        pd.DataFrame: a cleaned dataframe
        
    Example:
    >>> data = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Ana', 'Pedro', 'Maria']})
    >>> validade_athletes_columns(data)
    Traceback (most recent call last):
        ...
    KeyError: 'The given dataframe is missing columns'
    >>> data = pd.DataFrame({'ID': [1], 'Name': ['Carlos'], 'Sex': ['M'], 'Age': [23], 'Height': [160.0], 'Weight': [55.0], 'Team': ['Brazil'], 'NOC': ['BRA'], 'Games': ['2016 Summer'], 'Year': [2016], 'Season': ['Summer'], 'City': ['Rio'], 'Sport': ['Swimming'], 'Event': ['200m Freestyle'], 'Medal': [None]})
    >>> validade_athletes_columns(data)
    
    """
    required_columns = ['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError("The given dataframe is missing columns")


def medals_to_int(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe DataFrame com coluna 'Medal' e converte valores string para inteiros.
    0: Sem medalha; 1: Bronze; 2: Prata; 3: Ouro.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Medal'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Medal' convertida para inteiros.
    
    Example
    ----------
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': ['Gold', 'Gold', 'Silver', 'Bronze', np.nan]  })
    >>> df = medals_to_int(data)
    >>> print(df['Medal'].tolist())
    [3.0, 3.0, 2.0, 1.0, 0.0]
    
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': [np.nan, 'Bronze', 'Bronze', 'Bronze', np.nan]  }) 
    >>> df = medals_to_int(data)
    >>> print(df['Medal'].tolist())
    [0.0, 1.0, 1.0, 1.0, 0.0]
    
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': [np.nan, np.nan, np.nan, np.nan, np.nan]  }) 
    >>> df = medals_to_int(data)
    >>> print(df['Medal'].tolist())
    [0.0, 0.0, 0.0, 0.0, 0.0]
    """
    try:
        df.loc[:, 'Medal'] = df['Medal'].map({'Gold': 3, 'Silver': 2, 'Bronze': 1})
        df['Medal'] = df['Medal'].infer_objects().fillna(0)
        df.loc[:, 'Medal'] = df['Medal'].astype(int)
        
    except KeyError:
        print(
            f"The given dataframe has no column 'Medal', consider replacing it.")
        quit()
    else:
        return df


def transform_athletes_df_to_paralympics_format(athletes_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma o DataFrame de atletas olímpicos no formato utilizado pelos DataFrames paralímpicos

    Args:
        athletes_df (pd.DataFrame): DataFrame contendo os dados dos atletas olímpicos com as colunas:

    Returns:
        pd.DataFrame: Um DataFrame formatado como os DataFrames paralímpicos, mas com os dados das olimpíadas
    """
    athletes_df = athletes_df[athletes_df['Year'] >= 1960]

    olympic_df = athletes_df.groupby(['NOC', 'Year', 'Season']).agg(
        Gold=('Medal', lambda x: (x == 'Gold').sum()),
        Silver=('Medal', lambda x: (x == 'Silver').sum()),
        Bronze=('Medal', lambda x: (x == 'Bronze').sum()),
        Men=('Sex', lambda x: (x == 'M').sum()),
        Women=('Sex', lambda x: (x == 'F').sum())
    ).reset_index()

    # Calcula os totais e os atribui para suas respectivas novas colunas
    olympic_df['M_Total'] = olympic_df['Gold'] + olympic_df['Silver'] + olympic_df['Bronze']
    olympic_df['P_Total'] = olympic_df['Men'] + olympic_df['Women']

    return olympic_df


def urbanization_rename_countries(df: pd.DataFrame) -> pd.DateOffset:
    """Função que renomeia os países com nomes diferentes/em conflito internacional
    para padronizar com os outros DataFrames.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Country' para renomear.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Country' renomeada.
    """
    try:
        countries = {
            "United States of America": "USA",
            "Côte d'Ivoire": "Ivory Coast",
            "Korea, Republic of": "South Korea",
            "Korea, Dem. People's Rep. of": "North Korea",
            "Czechia": "Czech Republic",
            "Russian Federation": "Russia",
            "United Kingdom": "UK",
            "Iran (Islamic Republic of)": "Iran",
            "Netherlands (Kingdom of the)": "Netherlands",
            "China, Taiwan Province of": "Taiwan",
            "Trinidad and Tobago": "Trinidad",
            "Türkiye": "Turkey",
            "Venezuela (Bolivarian Rep. of)": "Venezuela",
            "Viet Nam": "Vietnam",
            "Moldova, Republic of": "Moldova",
            "Syrian Arab Republic": "Syria",
            "North Macedonia": "Macedonia",
            "Curaçao": "Curacao",
            "Tanzania, United Republic of": "Tanzania",
        }
        df['Country'] = df['Country'].replace(countries)
    except KeyError:
        print(
            f"The given dataframe has no column 'Country', consider replacing it.")
        quit()
    else:
        return df


def map_name_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Função que normaliza os nomes dos países para o padrão do Geopandas. Função similar a rename_countries

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Country' para renomear.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Country' renomeada.
    """
    try:
        countries = {
            "USA": "United States of America",
            "UK": "United Kingdom",
            "Trinidad": "Trinidad and Tobago",
            "Macedonia": "North Macedonia",
            "Czech Republic": "Czechia",
            "Ivory Coast": "Côte d'Ivoire",
        }
        
        df['Country'] = df['Country'].replace(countries)
    except KeyError:
        print(
            f"The given dataframe has no column 'Country', consider replacing it.")
        quit()
    else:
        return df


def aggregate_medals_by_event_team(athletes_df: pd.DataFrame) -> pd.DataFrame:
    """Função que recebe um DataFrame de atletas e retorna um DataFrame com as medalhas agregadas por evento e time,
    para evitar medalhas duplicadas (ex: 11 medalhas de ouro para o mesmo time no mesmo evento, por ter 11 atletas).

    Args:
        athletes_df (pd.DataFrame): df dos atletas

    Returns:
        pd.DataFrame: dataframe com as medalhas agregadas por evento e time
    
    Examples:
    >>> data = pd.DataFrame({'Event': ['100m', '100m', '100m', '100m', '100m'], 'Team': ['Brazil', 'Brazil', 'Brazil', 'Brazil', 'Brazil'], 'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'BRA'], 'Year': [2016, 2016, 2016, 2016, 2016], 'Games': ['2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer'], 'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Summer'], 'City': ['Rio', 'Rio', 'Rio', 'Rio', 'Rio'], 'Sport': ['Athletics', 'Athletics', 'Athletics', 'Athletics', 'Athletics'], 'Medal': ['Gold', 'Gold', 'Gold', 'Gold', 'Gold']})
    >>> df = aggregate_medals_by_event_team(data)
    >>> print(df['Medal'].tolist())
    ['Gold']
    """
    # Group the data by relevant columns and take the first non-null medal for the team in each event
    aggregated_df = athletes_df.groupby(
        ['Event', 'Team', 'NOC', 'Year', 'Games', 'Season', 'City', 'Sport'],
        as_index=False
    ).agg({
        'Medal': 'first'  # Takes the first non-null medal for the team in each event
    })
    
    return aggregated_df


if __name__ == "__main__":
     doctest.testmod(verbose=False)
