"""Módulo para comparação entre o crescimento da população urbana (percentual) e o crescimento da quantidade
média de medalhas ganhas por olimpíada para países nos últimos 50 anos.
Scatterplot para analisar a Urbanização Percentual X Densidade Urbana de Medalhas (qtd. de medalhas por habitante urbano).
"""
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *


def prepare_2016_medalist_urbanization_analysis(athletes_df: pd.DataFrame, urbanization_df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    """Função que gera um scatterplot com a relação entre a urbanização percentual e a densidade de medalhas por habitante urbano.
    
    Args:
        athletes_df (pd.DataFrame): DataFrame com dados dos atletas.
        urbanization_df (pd.DataFrame): DataFrame com dados de urbanização.
        noc_df (pd.DataFrame): DataFrame com dados de NOC.
    Returns:
        pd.DataFrame: DataFrame com dados de medalistas e urbanização em 2016.
    """
    # Filtragem dos atletas medalhistas para Análise e união com os dados de urbanização
    athletes_df.loc[:, 'Medal'] = athletes_df['Medal'].apply(lambda x: 1 if x in [1, 2, 3] else 0) # Só queremos saber se ganhou ou não
    athletes_2016 = athletes_df[athletes_df['Year'] == 2016]
    medal_count_per_country_2016 = athletes_2016.groupby('NOC')['Medal'].sum().reset_index()
    medal_count_per_country_2016.rename(columns={'Medal': 'Medalists'}, inplace=True)

    # Merge com noc_df pra mappear NOC no nome do país
    medal_count_per_country_2016 = pd.merge(medal_count_per_country_2016, noc_df[['NOC', 'Country']], on='NOC', how='left')
    medal_count_per_country_2016 = medal_count_per_country_2016[medal_count_per_country_2016['Medalists'] > 0]
    urbanization_2016 = urbanization_df[urbanization_df['Year'] == 2016]

    # Merge contagem de medalhistas com dados de urbanização
    data_2016 = pd.merge(medal_count_per_country_2016, urbanization_2016[['Country', 'Pop_Absolute', 'Urban_Pop_Percent']], on='Country', how='left')
    data_2016 = data_2016[~data_2016['Country'].isin(['Kosovo', 'Individual Olympic Athletes'])] # Não temos dados de urbanização de Kosovo

    # Preparando data_2016 para visualização
    data_2016['Pop_Absolute'] = data_2016['Pop_Absolute'].astype(float)
    data_2016['Pop_Absolute'] = data_2016['Pop_Absolute'] * 1000 # Convertendo de milhares para absoluto
    data_2016['Urban_Pop_Percent'] = data_2016['Urban_Pop_Percent'].astype(float)
    data_2016['Urban_Pop_Absolute'] = data_2016['Pop_Absolute'] * (data_2016['Urban_Pop_Percent'] / 100)
    data_2016['Urban_Medalist_Density'] = data_2016['Medalists'] / data_2016['Urban_Pop_Absolute']
    data_2016 = data_2016.sort_values(by='Urban_Pop_Percent')
    
    return data_2016


def save_scatterplot_2016_medalist_urbanization(data_2016: pd.DataFrame) -> None:
    """Função que gera um scatterplot com a relação entre a urbanização percentual e a densidade de medalhas por habitante urbano.
    
    Args:
        data_2016 (pd.DataFrame): DataFrame com dados de medalistas e urbanização em 2016.
    """
    # Scatterplot com Seaborn
    sns.set_theme(style="whitegrid")
    sns.set_palette("rocket")

    scatterplot = sns.scatterplot(x='Urban_Pop_Percent', y='Urban_Medalist_Density', data=data_2016, size='Medalists', sizes=(10, 100), legend=False)
    scatterplot.set_yscale('log') # Escala logarítmica para melhor visualização

    scatterplot.set_title('Urbanização X Densidade Urbana de Medalhas (2016)')
    scatterplot.set_xlabel('População Urbana (%)')
    scatterplot.set_ylabel('Medalhas por Habitante Urbano')

    # Identificando o top 5 e bottom 5 por Urban_Medalist_Density; também pegando o top 5 por medalhistas
    top_5_countries = data_2016.nlargest(5, 'Urban_Medalist_Density')
    bottom_5_countries = data_2016.nsmallest(5, 'Urban_Medalist_Density')
    most_medalists = data_2016.nlargest(5, 'Medalists')
    brazil = data_2016[data_2016['Country'] == 'Brazil']

    # Anotando o scatterplot com os países
    colorir = [top_5_countries, bottom_5_countries, most_medalists, brazil]
    colors = ['seagreen', '#e35252', '#d67e20', '#037bfc']
    font_sizes = [7, 7, 6, 6]
    for i, df in enumerate(colorir):
        for _, row in df.iterrows():
            scatterplot.text(row['Urban_Pop_Percent'], row['Urban_Medalist_Density'], row['Country'], color=colors[i], weight='bold', fontsize=font_sizes[i])

    # Save the scatterplot
    scatterplot.figure.savefig('graphs/urban_medal_density.png', dpi=500, bbox_inches='tight')


# GeoPandas para visualização geográfica
def prepare_map_visualization_data(athletes_df: pd.DataFrame, urbanization_df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    """Função para preparar os dados para entrada da função de visualização geográfica.

    Args:
        athletes_df (pd.DataFrame): DataFrame com dados dos atletas.
        urbanization_df (pd.DataFrame): DataFrame com dados de urbanização.
        noc_df (pd.DataFrame): DataFrame com dados de NOC.

    Returns:
        pd.DataFrame: DataFrame com os dados de medalistas e urbanização para visualização geográfica.
    """
    # Preparação da base de atletas
    athletes_df.loc[:, 'Medal'] = athletes_df['Medal'].apply(lambda x: 1 if x in [1, 2, 3] else 0) # Só queremos saber se ganhou ou não
    athletes_df = athletes_df[athletes_df['Year'].between(1956, 2016)]
    medal_count_per_country_per_year = athletes_df.groupby(['Year', 'NOC'])['Medal'].sum().reset_index()
    medal_count_per_country_per_year.rename(columns={'Medal': 'Medalists'}, inplace=True)
    
    # Merge com noc_df pra mappear NOC no nome do país
    medal_count_per_country_per_year = pd.merge(medal_count_per_country_per_year, noc_df[['NOC', 'Country']], on='NOC', how='left')
    medal_count_per_country_per_year = medal_count_per_country_per_year[medal_count_per_country_per_year['Medalists'] > 0]
    
    # Preparação da base de urbanização
    urbanization_df = urbanization_df.rename(columns={'Country Name': 'Country'})
    urbanization_df['Year'] = urbanization_df['Year'].astype(int)
    urbanization_df = urbanization_df[urbanization_df['Year'].between(1956, 2016)]

    # Merge dos dados de medalhas com os dados de urbanização
    data = pd.merge(medal_count_per_country_per_year, urbanization_df, on=['Country', 'Year'], how='left')
    data = data[~data['Country'].isin(['Kosovo', 'Individual Olympic Athletes'])] # Não temos dados de urbanização de Kosovo
    
    # Tratamento de dados faltantes
    data = data[data['Urban_Pop_Percent'] != 'NOT APPLICABLE']
    
    return data


def calculate_dynamic_growth(data: pd.DataFrame, value_column: str) -> pd.DataFrame:
    """Calcula o crescimento percentual de o valor especificado por coluna entre o primeiro e o último ano disponível do país.

    Args:
        data (pd.DataFrame): df com colunas: ,Year,NOC,Medalists,Country,Pop_Absolute,Urban_Pop_Percent
        value_column (str): Colunas para calcular crescimento (e.g. 'Medalists' or 'Urban_Pop_Percent').

    Returns:
        pd.DataFrame: Dataframe com País e Crescimento Percentual daquela coluna.
    """
    # Pega primeiro e último ano disponível para cada país
    first_year = data.groupby('Country').first().reset_index()[['Country', 'Year', value_column]]
    last_year = data.groupby('Country').last().reset_index()[['Country', 'Year', value_column]]

    # Renomeia colunas para facilitar merge
    first_year.rename(columns={value_column: f"{value_column}_first", 'Year': 'First_Year'}, inplace=True)
    last_year.rename(columns={value_column: f"{value_column}_last", 'Year': 'Last_Year'}, inplace=True)
    
    # Torna coluna em float
    first_year['First_Year'] = first_year['First_Year'].astype(float)
    last_year['Last_Year'] = last_year['Last_Year'].astype(float)

    # Merge first and last year dataframes
    growth_df = pd.merge(first_year, last_year, on='Country')
    growth_df.to_csv(f'data/df_checkpoints/growth_{value_column}_checkpoint.csv', index=False) # Checkpoint para análise
    
    column_growth = (growth_df[f'{value_column}_first'].astype(float) - growth_df[f'{value_column}_last'].astype(float))
    year_growth = (growth_df['First_Year'] - growth_df['Last_Year']).astype(float)

    # Calcula crescimento percentual
    try:
        growth_df[f'{value_column}_Growth'] = (column_growth / year_growth) * 100
    except ZeroDivisionError: # Caso onde o primeiro e o último ano são iguais
        growth_df[f'{value_column}_Growth'] = 0
    
    return growth_df[['Country', f'{value_column}_Growth']]


def save_map_visualization(data: pd.DataFrame) -> None:
    """Função que gera a visualização geográfica dos dados com geopandas.

    Args:
        data (pd.DataFrame): dados preparados para visualização geográfica.
    """
    # Tratando inconsistências nos nomes dos países (de novo...)
    data = map_name_normalization(data)
    
    # Calcula o crescimento da população urbana e dos medalhistas
    urban_growth = calculate_dynamic_growth(data, 'Urban_Pop_Percent')
    medalist_growth = calculate_dynamic_growth(data, 'Medalists')

    # Carrega mapa do GeoPandas
    world = gpd.read_file('data/world_map/ne_110m_admin_0_countries.shp')
    
    # Merge dos dados de crescimento com o geodataframe do mundo para plotagem
    world_urban = pd.merge(world, urban_growth, how='left', left_on='NAME', right_on='Country')
    world_medals = pd.merge(world, medalist_growth, how='left', left_on='NAME', right_on='Country')
    
    # Plot crescimento da urbanização
    plt.figure()
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    plt.subplots_adjust(wspace=0)  # Adjust the width space between subplots
    world_urban.plot(column='Urban_Pop_Percent_Growth', cmap='Blues', legend=False, ax=ax[0], missing_kwds={'color': 'lightgrey'}, linewidth=0.25, edgecolor='black')
    ax[0].set_title('Urbanization Growth (First to Last Available Year)')

    # Plot crescimento de medalhistas
    world_medals.plot(column='Medalists_Growth', cmap='Reds', legend=False, ax=ax[1], missing_kwds={'color': 'lightgrey'}, linewidth=0.25, edgecolor='black')
    ax[1].set_title('Medalists Growth (First to Last Available Year)')
    
    fig.suptitle('Comparison of Growth in Urbanization and Medalists (1956-2016)', fontsize=18, weight='bold')
    plt.subplots_adjust(bottom=0.55)

    plt.savefig('graphs/geographic_growth.png', dpi=500, bbox_inches='tight')


# Função interna para encontrar países com nomes diferentes; alguns não existem no GeoPandas (e.g. Singapura)
def find_mismatched_countries(data: pd.DataFrame) -> pd.DataFrame:
    """Find countries in the data that have mismatched names compared to GeoPandas world data.

    Args:
        data (pd.DataFrame): DataFrame containing the country names to check.

    Returns:
        pd.DataFrame: DataFrame with country names that do not match GeoPandas world dataset.
    """
    # Load world boundaries from GeoPandas
    world = gpd.read_file('data/world_map/ne_110m_admin_0_countries.shp')
    
    # Perform a left merge to check which countries in 'data' don't have a match in the GeoPandas world dataset
    merged_data = pd.merge(data[['Country']].drop_duplicates(), world[['NAME']], left_on='Country', right_on='NAME', how='left')
    
    # Find the countries where the merge resulted in NaN in the 'name' column (meaning no match in GeoPandas)
    mismatched_countries = merged_data[merged_data['NAME'].isna()]
    
    return mismatched_countries[['Country']]
