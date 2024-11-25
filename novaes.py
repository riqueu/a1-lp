from src import data_cleaner as dc
from src import data_predictor as dp
from src import olympics_paralympics_pib_analysis as opp
import pandas as pd

try:
    # Criação dos DataFrames para Análise
    athletes_df = pd.read_csv('data/athlete_events.csv')
    noc_df = pd.read_csv('data/noc_regions.csv').rename(columns={'region': 'Country'})
    modified_medal_athlete_df = pd.read_csv('data/modified_medal_athlete.csv')
    summer_paralympics_df = pd.read_csv('data/summer_paralympics.csv')
    winter_paralympics_df = pd.read_csv('data/winter_paralympics.csv')
    urbanization_df = pd.read_csv('data/urbanization.csv')
    gdp_df = pd.read_csv("data/gdp/gdp.csv").drop(columns=['Code', 'Unnamed: 65'])

    # Limpeza Inicial dos DataFrames
    dc.validade_athletes_columns(athletes_df) # Verifica se o DataFrame de Atletas possui todas as colunas necessárias
    clean_athletes_df = dc.medals_to_int(athletes_df)
    clean_athletes_df = dp.predict_missing(clean_athletes_df)
    urbanization_df.columns = ['Year', 'Economy_Code', 'Country', 'Pop_Absolute', 'Pop_Missing', 'Urban_Pop_Percent', 'Urban_Pop_Percent_Missing']
    urbanization_df = urbanization_df[['Year', 'Country', 'Pop_Absolute', 'Urban_Pop_Percent']]
    urbanization_df = dc.urbanization_rename_countries(urbanization_df) # Renomear países para padrão do DataFrame de Atletas
    
    # Análise PIB x Medalhas: Luís Filipe
    combined_df = opp.prepare_data_for_analysis(athletes_df, summer_paralympics_df, winter_paralympics_df, gdp_df, noc_df)

    olympics_paralympics_correlation_matrix = opp.prepare_olympics_paralympics_analysis(combined_df)
    heatmap_olympics_paralympics_pib = opp.create_heatmap(olympics_paralympics_correlation_matrix, 
                                                          "Correlation Heatmap Between Total Olympic and Paralympic Medals")
    # heatmap_olympics_paralympics_pib.savefig("graphs/heatmap_olympics_paralympics_medals.png", dpi=300)
    heatmap_olympics_paralympics_pib.close()

    total_medals_gdp_correlation_matrix = opp.prepare_total_medals_gdp_analysis(combined_df)
    heatmap_total_medals_gdp = opp.create_heatmap(total_medals_gdp_correlation_matrix, 
                                                  "Correlation Heatmap Between Total Medals (Olympic and Paralympic) and GDP")
    # heatmap_total_medals_gdp.savefig("graphs/heatmap_total_medals_gdp.png", dpi=300)
    heatmap_total_medals_gdp.close()

    medals_gdp_correlation_matrix = opp.prepare_medals_categories_gdp_analysis(combined_df)
    heatmap_medals_categories_gdp = opp.create_heatmap(medals_gdp_correlation_matrix,
                                                        "Correlation Heatmap Between the Types of Medals Won in the Olympics and Paralympics")
    # heatmap_medals_categories_gdp.savefig("graphs/heatmap_medals_categories_gdp.png", dpi=300)
    heatmap_medals_categories_gdp.close()

    prepared_df = opp.prepare_2016_olympics_paralympics_pib_analysis(combined_df)
    scatterplot_opp_2016 = opp.create_scatterplot_olympics_paralympics_pib_2016(prepared_df)
    # scatterplot_opp_2016.savefig("graphs/scatterplot_olympics_paralympics_pib_2016.png", dpi=300)
    scatterplot_opp_2016.close()

    scatterplot_opp_2016_approximate = opp.create_scatterplot_olympics_paralympics_pib_2016(prepared_df, xlim=(0, 120), ylim=(0,120), zlim=(0, 4000))
    # scatterplot_opp_2016_approximate.savefig("graphs/scatterplot_olympics_paralympics_pib_2016_approximate.png")
    scatterplot_opp_2016_approximate.close()
    
    new_scatterplot = opp.create_scatterplot_olympics_paralympics_pib_2016_2d(prepared_df)
    new_scatterplot.savefig("graphs/scatterplot_olympics_paralympics_pib_2016_2d.png", dpi=500)
    new_scatterplot.close()

except FileNotFoundError:
    print("File not found, check if the path is correct.")
