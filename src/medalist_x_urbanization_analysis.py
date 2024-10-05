"""Módulo para comparação entre o crescimento da população urbana (percentual) e o crescimento da quantidade
média de medalhas ganhas por olimpíada para países nos últimos 50 anos.
Scatterplot para analisar a Urbanização Percentual X Densidade Urbana de Medalhas (qtd. de medalhas por habitante urbano).
"""
import pandas as pd
import geopandas as gpd
import seaborn as sns
from data_cleaner import *

def prepare_2016_medalist_urbanization_analysis(athletes_df: pd.DataFrame, urbanization_df: pd.DataFrame, noc_df: pd.DataFrame) -> pd.DataFrame:
    """Função que gera um scatterplot com a relação entre a urbanização percentual e a densidade de medalhas por habitante urbano.
    
    Args:
        athletes_df (pd.DataFrame): DataFrame com dados dos atletas.
        urbanization_df (pd.DataFrame): DataFrame com dados de urbanização.
        noc_df (pd.DataFrame): DataFrame com dados de NOC.
    """
    # Filtragem dos atletas medalhistas para Análise e união com os dados de urbanização
    athletes_2016 = athletes_df[athletes_df['Year'] == 2016]
    medal_count_per_country_2016 = athletes_2016.groupby('NOC')['Medal'].sum().reset_index()
    medal_count_per_country_2016.rename(columns={'Medal': 'Medalists'}, inplace=True)

    # Merge com noc_df pra mappear NOC no nome do país
    medal_count_per_country_2016 = pd.merge(medal_count_per_country_2016, noc_df[['NOC', 'region']], on='NOC', how='left')
    medal_count_per_country_2016 = medal_count_per_country_2016.rename(columns={'region': 'Country'})
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
    colors = ['seagreen', '#e35252', '#d67e20', '#14ad09']
    font_sizes = [7, 7, 6, 6]
    for i, df in enumerate(colorir):
        for _, row in df.iterrows():
            scatterplot.text(row['Urban_Pop_Percent'], row['Urban_Medalist_Density'], row['Country'], color=colors[i], weight='bold', fontsize=font_sizes[i])

    # Save the scatterplot
    scatterplot.figure.savefig('graphs/urban_medal_density.png', dpi=500, bbox_inches='tight')


# TODO: Usar GeoPandas para visualização geográfica
