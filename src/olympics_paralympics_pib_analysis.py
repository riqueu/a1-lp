"""Módulo para limpeza, organização e visualização de dados de Olimpíadas, Paralimpíadas e PIB."""

import pandas as pd
from data_cleaner import convert_athletes_df_to_paralympics_format, rename_countries_gdp


def add_country_from_noc(df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona a coluna 'Country' ao DataFrame a partir do DataFrame NOC.

    Args:
        df (pd.DataFrame): DataFrame no padrão do paralympics_df contendo a coluna 'NOC'.
        noc_df (pd.DataFrame): DataFrame que relaciona NOC com os respectivos países.

    Returns:
        pd.DataFrame: DataFrame resultante com a coluna 'Country' adicionada, incluindo
            as colunas 'Year', 'Country', 'NOC', 'Season', 'Gold', 'Silver', 'Bronze',
            'M_Total', 'Men', 'Women', 'P_Total'.

    Raises:
        KeyError: Se uma ou mais colunas necessárias não estiverem presentes no DataFrame.
        Exception: Se ocorrer um erro durante a mesclagem dos DataFrames.
    """
    try:
        df = df.merge(noc_df[['NOC', 'Country']], on='NOC', how='left')
        return df[['Year', 'Country', 'NOC', 'Season', 'Gold', 'Silver', 'Bronze', 'M_Total', 'Men', 'Women', 'P_Total']]
    except KeyError as error:
        raise KeyError(f"KeyError: Missing one or more required columns in the GDP DataFrame: {error}")
    except Exception as error:
        raise Exception(f"Failed to merge NOC with country: {str(error)}")


def pivot_gdp_to_long(gdp_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma o gdp_df do formato wide (com cada ano sendo uma coluna) para o long.

    Args:
        gdp_df (pd.DataFrame): DataFrame contendo dados do PIB com os anos como colunas.

    Returns:
        pd.DataFrame: DataFrame transformado em formato long, com as colunas 'Year', 'Country'
            e 'GDP', ordenado por 'Year e 'Country'.

    Raises:
        KeyError: Se uma ou mais colunas necessárias não estiverem presentes no DataFrame.
        Exception: Se ocorrer um erro durante o reshape do DataFrame.
    """
    try:
        # Transforma o DataFrame para o formato longo usando melt
        gdp_df = gdp_df.melt(id_vars=['Country Name'], var_name='Year', value_name='GDP')
        gdp_df['Year'] = pd.to_numeric(gdp_df['Year'], errors='coerce').dropna().astype(int)
        gdp_df = gdp_df.rename(columns={'Country Name': 'Country'})
        gdp_df = rename_countries_gdp(gdp_df)
        return gdp_df[['Year', 'Country', 'GDP']].sort_values(by=['Year', 'Country'])
    except KeyError as error:
        raise KeyError(f"KeyError: Missing one or more required columns in the GDP DataFrame: {error}")
    except Exception as error:
        raise Exception(f"Error transforming GDP DataFrame: {str(error)}")


def fill_nan_gdp_with_interpolation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preenche valores NaN na coluna 'GDP' usando interpolação linear.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'Country' e a coluna 'GDP'.

    Returns:
        pd.DataFrame: DataFrame com todos os valores NaN da coluna 'GDP' preenchidos 
        por interpolação linear.

    Raises:
        KeyError: Se uma ou mais colunas necessárias não estiverem presentes no DataFrame.
        Exception: Se ocorrer um erro durante a interpolação dos valores de GDP.
    """
    try:
        # Interpola valores NaN na coluna 'GDP' para cada país
        df['GDP'] = df.groupby('Country')['GDP'].transform(lambda group: group.interpolate(method='linear', limit_direction='both'))
        return df
    except KeyError as error:
        raise KeyError(f"KeyError: Missing one or more required columns in the GDP DataFrame: {error}")
    except Exception as error:
        raise Exception(f"Error interpolating GDP values: {str(error)}")


def prepare_data_for_analysis(athletes_df: pd.DataFrame, summer_paralympics_df: pd.DataFrame, winter_paralympics_df: pd.DataFrame, gdp_df: pd.DataFrame, noc_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Prepara os dados das Olimpíadas, Paralimpíadas e PIB para análise conjunta.

    Args:
        athletes_df (pd.DataFrame): DataFrame contendo dados dos atletas das Olimpíadas.
        summer_paralympics_df (pd.DataFrame): DataFrame contendo dados dos atletas das
            Paralimpíadas de Verão.
        winter_paralympics_df (pd.DataFrame): DataFrame contendo dados dos atletas das
            Paralimpíadas de Inverno.
        gdp_df (pd.DataFrame): DataFrame contendo dados do PIB por país e ano.
        noc_df (pd.DataFrame): DataFrame relacionando códigos NOC com países.

    Returns:
        pd.DataFrame: DataFrame combinado contendo dados das Olimpíadas, Paralimpíadas e PIB,
            ordenado por ano, país e evento.

    Raises:
        KeyError: Se uma ou mais colunas necessárias não estiverem presentes no DataFrame.
        Exception: Se ocorrer um erro durante a preparação dos dados para análise.
    """
    try:
        # Converte o DataFrame dos atletas para o formato apropriado
        olympics_df = convert_athletes_df_to_paralympics_format(athletes_df)

        # Prepara os DataFrames das Paralimpíadas de Verão e Inverno
        summer_paralympics_df = summer_paralympics_df.drop(columns=['Host_City', 'Host_Country', 'Country']).assign(Season='Summer')
        winter_paralympics_df = winter_paralympics_df.drop(columns=['Host_City', 'Host_Country', 'Country']).assign(Season='Winter')
        combined_paralympics_df = pd.concat([summer_paralympics_df, winter_paralympics_df], ignore_index=True).rename(columns={'Country_Code': 'NOC'})

        clean_olympics_df = add_country_from_noc(olympics_df, noc_df).assign(Event='Olympics')
        clean_paralympics_df = add_country_from_noc(combined_paralympics_df, noc_df).assign(Event='Paralympics')
        combined_events_df = pd.concat([clean_olympics_df, clean_paralympics_df], ignore_index=True)

        gdp_long_df = pivot_gdp_to_long(gdp_df)

        combined_df = pd.merge(combined_events_df, gdp_long_df, on=['Year', 'Country'], how='left')
        combined_df = fill_nan_gdp_with_interpolation(combined_df)

        # Exclui (poucas) linhas com NOCs problemáticos
        nocs_not_in_analysis = ['FRO', 'RPT', 'PRK', 'AHO', 'TPE', 'IVB', 'COK', 'MAC', 'IOA', 'IPP', 'PLE', 'IPA', 'LBN', 'TUV', 'NPA', 'SSD', 'ROT', 'RPC']
        combined_df = combined_df[~combined_df['NOC'].isin(nocs_not_in_analysis)]

        return combined_df.sort_values(by=['Year', 'Country', 'Event'])
    except KeyError as error:
        raise KeyError(f"KeyError: Missing one or more required columns in the dataframes:")
    except Exception as error:
        raise Exception(f"Error preparing data for analysis: {str(error)}")
