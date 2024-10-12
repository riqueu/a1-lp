from src import medalist_x_urbanization_analysis as mu
from src import age_analysis as aa
from src import data_cleaner as dc
from src import data_predictor as dp
from src import womens_participation_graphs as wpg
from src import womens_participation as wp
from src import physical_attributes_analysis as pa
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
    wp.clean_paralympic_atletes_dataset()
    olymp_df, olymp_countries_df, paralymp_df, paralymp_countries_df, olymp_sports_df, olymp_sports_bra_df, paralymp_sports_df, paralymp_sports_bra_df = wp.create_dataframes()

    # Análise de Densidade de Medalhas por População Urbana em 2016: Henrique
    data_2016 = mu.prepare_2016_medalist_urbanization_analysis(clean_athletes_df, urbanization_df, noc_df)
    scatterplot_2016 = mu.create_scatterplot_2016_medalist_urbanization(data_2016)
    scatterplot_2016.figure.savefig('graphs/urban_medal_density.png', dpi=500, bbox_inches='tight')
    # Visualização Geográfica do crescimento de medalhas por país e do crescimento urbano de um país: Henrique
    data_map_visualization = mu.prepare_map_visualization_data(clean_athletes_df, urbanization_df, noc_df)
    map_visualization = mu.create_map_visualization(data_map_visualization)
    map_visualization.savefig('graphs/geographic_growth.png', dpi=500, bbox_inches='tight')
    map_visualization.close()
    
    # Análise Idades: Jaime
    top_3_boxplot_outliers = aa.create_boxplot_top_3_esportes_outliers(clean_athletes_df)
    top_3_boxplot_outliers.savefig('graphs/bloxplot_top_3_highest_age_aplitude.png', format='png', dpi=300)
    top_3_boxplot_outliers.close()
    
    top_3_boxplot_most_awarded = aa.create_boxplot_top_3_esportes_most_awarded(clean_athletes_df)
    top_3_boxplot_most_awarded.savefig('graphs/boxplot_top_3_most_awarded.png', format='png', dpi=300)
    top_3_boxplot_most_awarded.close()
    
    boxplot_age_medal_status_brazil = aa.create_boxplot_age_medal_status_brazil(clean_athletes_df)
    boxplot_age_medal_status_brazil.savefig('graphs/boxplot_age_awarded_and_non_awarded_brazil.png', format='png', dpi=300)
    boxplot_age_medal_status_brazil.close()

    #Análise Participação Feminina: Walléria
    table_stds = wpg.create_table_of_stds()
    table_stds.savefig('graphs/female_participation/table_stds_olympics_and_paralympics_bra.png', format='png', dpi=300)
    table_stds.close()

    scatterplot_paralymp_score_bra_df = wpg.filter_paralymp_score_bra()
    scatterplot_paralymp_score_bra = wpg.plot_scatter_graph(scatterplot_paralymp_score_bra_df, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Paralympic Score (Brazil)', 'Score')
    scatterplot_paralymp_score_bra.savefig('graphs/female_participation/scatterplot_paralymp_score_bra.png', format='png', dpi=300)
    scatterplot_paralymp_score_bra.close()
    
    scatterplot_olymp_score_bra_df = wpg.filter_olympic_score_bra()
    scatterplot_olymp_score_bra = wpg.plot_scatter_graph(scatterplot_olymp_score_bra_df, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Men\'s Score X Women\'s Olympic Score (Brazil)', 'Score')
    scatterplot_olymp_score_bra.savefig('graphs/female_participation/scatterplot_olymp_score_bra.png', format='png', dpi=300)
    scatterplot_olymp_score_bra.close()

    scatterplot_paralymp_score_global_df = wpg.filter_paralymp_score_global()
    scatterplot_paralymp_score_global = wpg.plot_scatter_graph(scatterplot_paralymp_score_global_df, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Men\'s Score X Women\'s Paralympic Score', 'Score')
    scatterplot_paralymp_score_global.savefig('graphs/female_participation/scatterplot_paralymp_score_global.png', format='png', dpi=300)
    scatterplot_paralymp_score_global.close()

    scatterplot_olymp_score_global_df = wpg.filter_olympic_score_global()
    scatterplot_olymp_score_global = wpg.plot_scatter_graph(scatterplot_olymp_score_global_df, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Men\'s Score X Women\'s Olympic Score', 'Score')
    scatterplot_olymp_score_global.savefig('graphs/female_participation/scatterplot_olymp_score_global.png', format='png', dpi=300)
    scatterplot_olymp_score_global.close()
    
    # Análise dos Atributos Físicos dos Atletas: Carlos
    pa.attributes_sports_analysis(clean_athletes_df)
    pa.attributes_years_analysis(clean_athletes_df)
    
    # Análise PIB x Medalhas: Luís Filipe
    combined_df = opp.prepare_data_for_analysis(athletes_df, summer_paralympics_df, winter_paralympics_df, gdp_df, noc_df)

    olympics_paralympics_correlation_matrix = opp.prepare_olympics_paralympics_analysis(combined_df)
    heatmap_olympics_paralympics_pib = opp.create_heatmap(olympics_paralympics_correlation_matrix, 
                                                          "Correlation Heatmap Between Total Olympic and Paralympic Medals")
    heatmap_olympics_paralympics_pib.savefig("graphs/medals_gdp_correlation_graphs/heatmap_olympics_paralympics_medals.png", dpi=300)
    heatmap_olympics_paralympics_pib.close()

    total_medals_gdp_correlation_matrix = opp.prepare_total_medals_gdp_analysis(combined_df)
    heatmap_total_medals_gdp = opp.create_heatmap(total_medals_gdp_correlation_matrix, 
                                                  "Correlation Heatmap Between Total Medals (Olympic and Paralympic) and GDP")
    heatmap_total_medals_gdp.savefig("graphs/medals_gdp_correlation_graphs/heatmap_total_medals_gdp.png", dpi=300)
    heatmap_total_medals_gdp.close()

    medals_gdp_correlation_matrix = opp.prepare_medals_categories_gdp_analysis(combined_df)
    heatmap_medals_categories_gdp = opp.create_heatmap(medals_gdp_correlation_matrix,
                                                        "Correlation Heatmap Between the Types of Medals Won in the Olympics and Paralympics")
    heatmap_medals_categories_gdp.savefig("graphs/medals_gdp_correlation_graphs/heatmap_medals_categories_gdp.png", dpi=300)
    heatmap_medals_categories_gdp.close()

    prepared_df = opp.prepare_2016_olympics_paralympics_pib_analysis(combined_df)
    scatterplot_opp_2016 = opp.create_scatterplot_olympics_paralympics_pib_2016(prepared_df)
    scatterplot_opp_2016.savefig("graphs/medals_gdp_correlation_graphs/scatterplot_olympics_paralympics_pib_2016.png", dpi=300)
    scatterplot_opp_2016.close()

    scatterplot_opp_2016_approximate = opp.create_scatterplot_olympics_paralympics_pib_2016(prepared_df, xlim=(0, 120), ylim=(0,120), zlim=(0, 4000))
    scatterplot_opp_2016_approximate.savefig("graphs/medals_gdp_correlation_graphs/scatterplot_olympics_paralympics_pib_2016_approximate.png")
    scatterplot_opp_2016_approximate.close()

except FileNotFoundError:
    print("File not found, check if the path is correct.")
