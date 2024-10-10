from src import medalist_x_urbanization_analysis as mu
from src import age_analysis as aa
from src import data_cleaner as dc
from src import data_predictor as dp
import pandas as pd

try:
    # Criação dos DataFrames para Análise
    athletes_df = pd.read_csv('data/athlete_events.csv')
    noc_df = pd.read_csv('data/noc_regions.csv').rename(columns={'region': 'Country'})
    urbanization_df = pd.read_csv('data/urbanization.csv')
    gdp_df = pd.read_csv('data/gdp/gdp.csv')
    gdp_per_capita_df = pd.read_csv('data/gdp/gdp_per_capita.csv')

    # Limpeza Inicial dos DataFrames
    dc.validade_athletes_columns(athletes_df) # Verifica se o DataFrame de Atletas possui todas as colunas necessárias
    clean_athletes_df = dc.medals_to_int(athletes_df)
    clean_athletes_df = dp.predict_missing(clean_athletes_df)
    urbanization_df.columns = ['Year', 'Economy_Code', 'Country', 'Pop_Absolute', 'Pop_Missing', 'Urban_Pop_Percent', 'Urban_Pop_Percent_Missing']
    urbanization_df = urbanization_df[['Year', 'Country', 'Pop_Absolute', 'Urban_Pop_Percent']]
    urbanization_df = dc.urbanization_rename_countries(urbanization_df) # Renomear países para padrão do DataFrame de Atletas
    
    # Análise de Densidade de Medalhas por População Urbana em 2016
    data_2016 = mu.prepare_2016_medalist_urbanization_analysis(clean_athletes_df, urbanization_df, noc_df)
    scatterplot_2016 = mu.create_scatterplot_2016_medalist_urbanization(data_2016)
    scatterplot_2016.figure.savefig('graphs/urban_medal_density.png', dpi=500, bbox_inches='tight')
    
    # Visualização Geográfica do crescimento de medalhas por país e do crescimento urbano de um país
    data_map_visualization = mu.prepare_map_visualization_data(clean_athletes_df, urbanization_df, noc_df)
    map_visualization = mu.create_map_visualization(data_map_visualization)
    map_visualization.savefig('graphs/geographic_growth.png', dpi=500, bbox_inches='tight')
    
    # Análise Idades
    top_3_boxplot = aa.create_boxplot_top_3_esportes_outliers(clean_athletes_df)
    top_3_boxplot.savefig('graphs/bloxplot_top_3_highest_age_aplitude.png', format='png', dpi=300)


except FileNotFoundError:
    print("File not found, check if the path is correct.")
