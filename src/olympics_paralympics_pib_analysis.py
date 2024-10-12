"""Módulo para limpeza, organização e visualização de dados de Olimpíadas, Paralimpíadas e PIB."""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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

        # Exclui (poucas) linhas com NOCs problemáticos
        nocs_not_in_analysis = ['FRO', 'RPT', 'PRK', 'AHO', 'TPE', 'IVB', 'COK', 'MAC', 'IOA', 'IPP', 'PLE', 'IPA', 'LBN', 'TUV', 'NPA', 'SSD', 'ROT', 'RPC']
        combined_df = combined_df[~combined_df['NOC'].isin(nocs_not_in_analysis)]

        combined_df = fill_nan_gdp_with_interpolation(combined_df)

        # Converte o PIB para bilhões
        combined_df['GDP'] = combined_df['GDP'] / 1e9

        return combined_df.sort_values(by=['Year', 'Country', 'Event'])
    except KeyError as error:
        raise KeyError(f"KeyError: Missing one or more required columns in the dataframes:")
    except Exception as error:
        raise Exception(f"Error preparing data for analysis: {str(error)}")


def prepare_total_medals_gdp_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para análise de correlação entre medalhas e PIB.

    Args:
        data (pd.DataFrame): DataFrame contendo colunas 'Gold', 'Silver', 'Bronze' e 'GDP'.

    Returns:
        pd.DataFrame: Matriz de correlação entre as medalhas de ouro, prata, bronze e o PIB.
    """
    correlation_matrix = data[['M_Total', 'GDP']].corr()

    return correlation_matrix


def prepare_medals_categories_gdp_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para análise de correlação entre medalhas e PIB.

    Args:
        data (pd.DataFrame): DataFrame contendo colunas 'Gold', 'Silver', 'Bronze' e 'GDP'.

    Returns:
        pd.DataFrame: Matriz de correlação entre as medalhas de ouro, prata, bronze e o PIB.
    """
    correlation_matrix = data[['Gold', 'Silver', 'Bronze', 'GDP']].corr()

    return correlation_matrix


def prepare_olympics_paralympics_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para análise de correlação entre medalhas nas Olimpíadas e nas Paralimpíadas.

    Args:
        data (pd.DataFrame): DataFrame contendo colunas 'Country', 'Event', 'Gold', 'Silver' e 'Bronze'.

    Returns:
        pd.DataFrame: Matriz de correlação entre as medalhas de ouro, bronze e prata das Olimpíadas e Paralimpíadas.
    """
    grouped_data = data.groupby(['Country', 'Event']).agg({
        'M_Total': 'sum'
    }).reset_index()

    # Pivota o DataFrame para ter eventos como colunas
    heatmap_data = grouped_data.pivot_table(index='Country', columns='Event', values=['M_Total'], fill_value=0)

    # Calcula a correlação entre as medalhas de ouro, prata e bronze
    correlation_matrix = heatmap_data.corr()

    return correlation_matrix


def prepare_2016_olympics_paralympics_pib_analysis(data: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para análise das medalhas nas Olimpíadas e Paralimpíadas e 
    PIB dos países em 2016.

    Args:
        data (pd.DataFrame): DataFrame contendo as colunas 'Year', 'Country', 
            'Event', 'M_Total' e 'GDP'.

    Returns:
        pd.DataFrame: DataFrame preparado com as colunas 'Country', 'M_Olympics', 
            'M_Paralympics' e 'GDP' para o ano de 2016.
    """
    # Filtra os dados para incluir apenas o ano de 2016 e países com mais de 5 medalhas
    data_2016 = data[(data['Year'] == 2016) & (data['M_Total'] > 5)]
    
    # Agrupa os dados por país e evento (Olimpíadas e Paralimpíadas)
    grouped_data = data_2016.groupby(['Country', 'Event']).agg({
        'M_Total': 'sum',
        'GDP': 'mean'
    }).reset_index()

    # Cria colunas separadas para Olimpíadas e Paralimpíadas
    olympics_data = grouped_data[grouped_data['Event'] == 'Olympics'].rename(columns={'M_Total': 'M_Olympics'})
    paralympics_data = grouped_data[grouped_data['Event'] == 'Paralympics'].rename(columns={'M_Total': 'M_Paralympics'})

    # Une os dados de Olimpíadas e Paralimpíadas
    merged_data = pd.merge(olympics_data[['Country', 'M_Olympics', 'GDP']], paralympics_data[['Country', 'M_Paralympics']], 
                           on='Country', how='outer').fillna(0)

    return merged_data


def create_heatmap(correlation_matrix: pd.DataFrame, title: str) -> None:
    """
    Cria um heatmap de correlação com a matrix de correlação e título passados.

    Args:
        data (pd.DataFrame): Matrix de correlação.

    Returns:
        plt: Objeto do tipo matplotlib.pyplot com o heatmap.
    """
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    
    plt.title('Heatmap de Correlação entre Medalhas de Ouro, Prata e Bronze')
    
    return plt


def create_scatterplot_olympics_paralympics_pib_2016(data_2016: pd.DataFrame, xlim: tuple = None, ylim: tuple = None, zlim: tuple = None) -> None:
    """
    Cria um gráfico de dispersão 3D que mostra a relação entre medalhas nas
    Olimpíadas, nas Paralimpíadas e PIB dos países em 2016.

    Args:
        data (pd.DataFrame): DataFrame preparado com colunas 'Country', 
            'M_Olympics', 'M_Paralympics' e 'GDP'.

    Returns:
        plt: Objeto do tipo matplotlib.pyplot com o scatterplot.
    """
    # Cria a figura e os eixos 3D
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plota os dados
    ax.scatter(data_2016['M_Olympics'], data_2016['M_Paralympics'], 
               data_2016['GDP'], c='blue', marker='o', alpha=0.6)

    # Adiciona labels aos eixos
    ax.set_xlabel('Total Medals at the Olympics')
    ax.set_ylabel('Total Medals at the Paralympics')
    ax.set_zlabel('GDP (in billions)')
    ax.set_title('3D Dispersion: Medals in the Olympics and Paralympics vs GDP (2016)')

    ax.view_init(elev=20, azim=-70)

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if zlim:
        ax.set_zlim(zlim)

    return plt
