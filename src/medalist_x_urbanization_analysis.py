"""Módulo para Análise Análise da média geral de medalhas (ouro, prata, bronze) ganhas por 
atletas de países diferentes e relacionar a quantidade com o desenvolvimento do país (usando o PIB e a Urbanização). 
Usando o geopandas para representação gráfica."""
import pandas as pd
import geopandas as gpd
import seaborn as sns
from data_cleaner import *

# Criação dos DataFrames para Análise
athletes_df = pd.read_csv('../data/athlete_events.csv') # "ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"
noc_df = pd.read_csv('../data/noc_regions.csv') # NOC,region,notes
urbanization_df = pd.read_csv('../data/urbanization.csv') # 'Year', 'Economy_Code', 'Country', 'Urban_Pop_Absolute', 'Urban_Pop_Missing', 'Urban_Pop_Percent', 'Urban_Pop_Percent_Missing'
gdp_per_capita_df = pd.read_csv('../data/gdp/gdp_per_capita.csv') # Country Name,Code,1960,1961,1962,1963, ..., 2020
gdp_per_capita_growth_df = pd.read_csv('../data/gdp/gdp_per_capita_growth.csv') # Country Name,Code,1960,1961,1962,1963, ..., 2020


# Limpeza dos DataFrames TODO: Limpeza GDP e Urbanization
athletes_df = medals_to_int(athletes_df)
athletes_df = predict_missing(athletes_df)
urbanization_df.columns = ['Year', 'Economy_Code', 'Country', 'Urban_Pop_Absolute', 'Urban_Pop_Missing', 'Urban_Pop_Percent', 'Urban_Pop_Percent_Missing']
urbanization_df = urbanization_df[['Year', 'Country', 'Urban_Pop_Percent']]
urbanization_df['Country'] = urbanization_df['Country'].replace('United States of America', 'USA')
gdp_per_capita_growth_df = gdp_per_capita_growth_df.loc[:, ~gdp_per_capita_growth_df.columns.str.contains('^Unnamed')]

# TODO: Verificar se População Urbana Absoluta seria melhor que % da População Urbana
# FIXME: Peso das medalhas sendo contado como várias medalhas, influenciando na contagem
# Filtragem dos atletas medalhistas para Análise; Cálculo da quantidade de medalhas por Comitê Olímpico Nacional (NOC)
medals_by_country_2016 = athletes_df[(athletes_df['Medal'] > 0) & (athletes_df['Year'] == 2016)].groupby(['NOC', 'Medal']).size().unstack(fill_value=0).reset_index()
medals_by_country_2016.columns = ['NOC', 'Bronze', 'Gold', 'Silver']
medals_by_country_2016['Total_Medals'] = medals_by_country_2016[['Bronze', 'Silver', 'Gold']].sum(axis=1)
medals_by_country_2016 = pd.merge(medals_by_country_2016, noc_df[['NOC', 'region']], on='NOC', how='right')
medals_by_country_2016 = medals_by_country_2016.rename(columns={'region': 'Country'})

# Reformatar dados de urbanização para o ano de 2016
urbanization_2016 = urbanization_df[urbanization_df['Year'] == 2016]

# Mesclar os dados de medalhas e urbanização
data_2016 = pd.merge(medals_by_country_2016, urbanization_2016, on='Country', how='left')
data_2016['Urban_Pop_Percent'] = data_2016['Urban_Pop_Percent'].astype(float)

data_2016.to_csv('data_2016.csv')

# FIXME: Wrong medal count
# Scatter plot: Urbanization percentage vs total medals for 2016
scatterplot = sns.scatterplot(data=data_2016, x='Urban_Pop_Percent', y='Total_Medals', hue='Country', legend=False)
scatterplot.set_title('Urbanization Percentage vs Total Medals for 2016')
# Ticks on the x-axis
scatterplot.set_xticks(range(0, 101, 20))
scatterplot.set_xticklabels([f'{i}%' for i in range(0, 101, 20)])

# Save the figure
scatterplot.figure.savefig("out_2016.png")


# Gráficos de evolução com Seaborn

# Usar GeoPandas para visualização geográfica
