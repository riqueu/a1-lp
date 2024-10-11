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
    
    Example:
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
        df = df.copy()
        df.loc[:, 'Medal'] = df['Medal'].map({'Gold': 3, 'Silver': 2, 'Bronze': 1})
        df['Medal'] = df['Medal'].infer_objects().fillna(0)
        df.loc[:, 'Medal'] = df['Medal'].astype(int)
        
    except KeyError:
        print(
            f"The given dataframe has no column 'Medal', consider replacing it.")
        quit()
    else:
        return df


def convert_athletes_df_to_paralympics_format(athletes_df: pd.DataFrame) -> pd.DataFrame:
    """TODO:"""
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
        
    Example:
    >>> data = pd.DataFrame({'Country': ['USA', 'UK', 'Trinidad', 'Macedonia', 'Czech Republic', 'Ivory Coast']})
    >>> df = urbanization_rename_countries(data)
    >>> print(df['Country'].tolist())
    ['United States of America', 'United Kingdom', 'Trinidad and Tobago', 'North Macedonia', 'Czechia', "Côte d'Ivoire"]
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
    
    
def rename_countries_gdp(df: pd.DataFrame) -> pd.DataFrame:
    countries = {
        "Bahamas, The": "Bahamas",
        "Curacao": "Curacao",
        "Iran, Islamic Rep.": "Iran",
        "Russian Federation": "Russia",
        "Korea, Rep.": "South Korea",
        "Syrian Arab Republic": "Syria",
        "Trinidad and Tobago": "Trinidad",
        "United Kingdom": "UK",
        "United States": "USA",
        "Venezuela, RB": "Venezuela",
        "Bolivia": "Boliva",
        "Egypt, Arab Rep.": "Egypt",
        "Cote d'Ivoire": "Ivory Coast",
        "Congo, Rep.": "Republic of Congo",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Virgin Islands (U.S.)": "Virgin Islands, US",
        "Eswatini": "Swaziland",
        "Antigua and Barbuda": "Antigua",
        "Lao PDR": "Laos",
        "Gambia, The": "Gambia",
        "Yemen, Rep.": "Yemen",
        "St. Vincent and the Grenadines": "Saint Vincent",
        "Slovak Republic": "Slovakia",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Brunei Darussalam": "Brunei",
        "Cabo Verde": "Cape Verde",
        "North Macedonia": "Macedonia",
        "St. Kitts and Nevis": "Saint Kitts",
        "St. Lucia": "Saint Lucia",
        "Micronesia, Fed. Sts.": "Micronesia",
    }
    try:
        df['Country'] = df['Country'].replace(countries)
    except KeyError:
        print(
            f"The given dataframe has no column 'Country', consider replacing it.")
        quit()
    else:
        return df


def clean_paralympic_atletes_dataset():
    """Função que padroniza os dados do dataset medal_athletes.csv com os dados dos outros datasets com informações das paralimpíadas e olimpíadas e cria um dataset modified_medal_athletes.csv com as modificações
    """
    df = pd.read_csv("data/medal_athlete.csv")
    df.rename(columns={column: column.capitalize() for column in df.columns}, inplace=True)
    df = medals_to_int(df)
    df['Sex'] = np.nan
    df.loc[df['Event'].str.contains('Men', case=False, na=False), ['Sex']] = 'M'
    df.loc[df['Event'].str.contains('Women', case=False, na=False), ['Sex']] = 'F'

    # Variaveis auxiliares para verificar se a quantidade de atletas removidos esta correta
    identified_athletes = df[(df['Sex'] == 'F') | (df['Sex'] == 'M')]
    unidentified_athletes = df[df['Sex'].isna()]
    aux_1 = identified_athletes['Athlete_name'].unique().astype(str)
    aux_2 = unidentified_athletes['Athlete_name'].unique().astype(str)

    # Atualiza o dataframe com o genero dos atletas que foram distinguiveis
    df_auxiliar_map = df.groupby(['Athlete_name']).first()
    df_auxiliar_map = df_auxiliar_map['Sex'].to_dict()
    df['Sex'] = df['Athlete_name'].map(df_auxiliar_map)

    # Dropa os atletas em que nao foi possivel descobrir o genero
    df.dropna(subset=['Sex'], inplace=True)

    # Intersecao dos atletas que nao possuem identificacao alguma de genero com os atletas do dataset modificado
    # print(np.intersect1d(df['Athlete_name'].to_numpy(), np.setdiff1d(aux_2, aux_1)))
    # print(df['Athlete_name'].nunique())
    
    df.to_csv('data/modified_medal_athlete.csv')


def map_name_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Função que normaliza os nomes dos países para o padrão do Geopandas. Função similar a rename_countries

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Country' para renomear.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Country' renomeada.
    
    Example:
    >>> data = pd.DataFrame({'Country': ['USA', 'UK', 'Trinidad', 'Macedonia', 'Czech Republic', 'Ivory Coast']})
    >>> df = map_name_normalization(data)
    >>> print(df['Country'].tolist())
    ['United States of America', 'United Kingdom', 'Trinidad and Tobago', 'North Macedonia', 'Czechia', "Côte d'Ivoire"]
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
