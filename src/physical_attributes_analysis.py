"""Modulo com as funcoes para a hipotese do perfil fisico dos atletas"""
import numpy as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from data_cleaner import medals_to_int
from data_predictor import *
from coeficient_functions import *

original = pd.read_csv('data\\athlete_events.csv')
original = medals_to_int(original)
# df = predict_missing(original.copy())

# Classificacao dos esportes em 7 categorias, dada pelo ChatGpt
sport_map = {
    'Basketball': 'invasao','Judo': 'combate','Football': 'invasao','Tug-Of-War': 'invasao','Speed Skating': 'marca','Cross Country Skiing': 'marca',
    'Athletics': 'marca','Ice Hockey': 'invasao','Swimming': 'marca','Badminton': 'rede/parede','Sailing': 'marca','Biathlon': 'tecnico-combinatorio',
    'Gymnastics': 'tecnico-combinatorio','Art Competitions': 'tecnico-combinatorio','Alpine Skiing': 'marca','Handball': 'invasao','Weightlifting': 'marca',
    'Wrestling': 'combate','Luge': 'tecnico-combinatorio','Water Polo': 'invasao','Hockey': 'invasao','Rowing': 'marca','Bobsleigh': 'tecnico-combinatorio',
    'Fencing': 'tecnico-combinatorio','Equestrianism': 'tecnico-combinatorio','Shooting': 'precisao','Boxing': 'combate','Taekwondo': 'combate','Cycling': 'marca',
    'Diving': 'marca','Canoeing': 'marca','Tennis': 'rede/parede','Modern Pentathlon': 'tecnico-combinatorio','Figure Skating': 'tecnico-combinatorio','Golf': 'precisao',
    'Softball': 'campo/taco','Archery': 'precisao','Volleyball': 'rede/parede','Synchronized Swimming': 'tecnico-combinatorio','Table Tennis': 'rede/parede',
    'Nordic Combined': 'tecnico-combinatorio','Baseball': 'campo/taco','Rhythmic Gymnastics': 'tecnico-combinatorio','Freestyle Skiing': 'marca','Rugby Sevens': 'invasao',
    'Trampolining': 'tecnico-combinatorio','Beach Volleyball': 'rede/parede','Triathlon': 'marca','Ski Jumping': 'marca','Curling': 'precisao',
    'Snowboarding': 'tecnico-combinatorio','Rugby': 'invasao','Short Track Speed Skating': 'marca','Skeleton': 'tecnico-combinatorio','Lacrosse': 'invasao',
    'Polo': 'invasao','Racquets': 'rede/parede','Motorboating': 'marca','Jeu De Paume': 'rede/parede'
}

def get_filters(df: pd.DataFrame) -> tuple:
    """ Funcao que recebe um dataframe e cria os filtros de esportes mais coerentes e esportes que o brasil mais ganhou.

    Args:
        df (pd.Dataframe): Datarame com os dados brutos.

    Returns:
        tuple: Uma lista com os 7 esportes mais coerentes, uma lista com o esporte mais coerente de cada uma das 7 categorias e uma lista com os 7 esportes que o Brasil mais ganhou.
    """
    # Classificacao dos esportes nas 7 categorias
    df = df.copy()
    df.loc[:, 'sport_class'] = df['Sport'].map(sport_map)

    # Filtro para os esportes mais coerentes
    coerentes = original[['Sport', 'Sex', 'Age', 'Height', 'Weight']].groupby('Sport').count()
    coerentes['complete'] = coerentes.apply(lambda x: x.sum()/(x.shape[0]*x.Sex), axis=1)
    coerentes = coerentes.reset_index().sort_values(by='complete', ascending=False).set_index('Sport')
    sports_complete_map = coerentes['complete'].to_dict()
    df.loc[:, 'complete'] = df['Sport'].map(sports_complete_map)
    df = df.sort_values(by='complete', ascending=False)
    top_sports_complete = list(sports_complete_map.keys())[:7]

    # Filtro para pegar os esporte mais coerente de cada categoria
    category = df.groupby('sport_class').first().reset_index()
    top_sports_complete_category = category.Sport.unique().tolist()

    # Filtro para os esportes mais premiados do Brasil
    df_brasil = df[df['NOC'] == 'BRA']
    df_medals_brasil = df_brasil[['Sport', 'Medal', 'Sex', 'Age', 'Height', 'Weight']].groupby('Sport').count()
    df_medals_brasil = df_medals_brasil.reset_index().sort_values(by='Medal', ascending=False)
    top_sports_brasil = df_medals_brasil.head(7).Sport.tolist()
    
    return top_sports_complete, top_sports_complete_category, top_sports_brasil


# df, cols_to_fix, cols_types, encoders = to_encoded(df)
# print(f'Colunas problematicas: {cols_to_fix}\nColunas com varios tipos: {cols_types}')
def attributes_sports_analysis(df: pd.DataFrame) -> None:
    """ Funcao que recebe um DataFrame e analisa as possiveis relacoes de associacao entre suas variaveis de atributos fisicos com os esportes.

    Args:
        df (pd.DataFrame): DataFrame com as variaveis.
    """
    # Obtem os filtros analise
    top_sports_complete, top_sports_complete_category, top_sports_brasil = get_filters(df)

    # Verificacao das associacoes dos atributos fisicos com as colunas de esporte (geral ou categorizado) para cada filtro
    """for filter_sport, name_filter in zip([top_sports_complete, top_sports_complete_category, top_sports_brasil], ['Top_complete', 'Top_complete_category', 'brasil']):
        print(f'Analisando o filtro: {name_filter}\n')
        df_filter = df[df['Sport'].isin(filter_sport)]
        for column_quali in ['Sport', 'sport_class']:
            print(f'--------------- Analisando associacao com {column_quali}:')
            for attribute in ['Age', 'Height', 'Weight']:
                r_2 = r2(df_filter, column_quali, attribute, False)
                print(f'Associacao entre {column_quali} e {attribute}')
                print(f'Coeficiente r_2 = {r_2}\n')
        print('\n\n\n')"""

    # E evidente que a os atributos fisicos estao mais associados ao proprio esporte do que a categoria dele
    # Idade e geralmente o atributo que tem menor associacao com o esporte
    # Para os esportes mais premiados do Brasil, os atributos parecem tem maior associacao com o esporte do que quando aplicado a outros esportes

    # Analise dos dados dos esportes mais premiados do Brasil
    df_top_sports = df[df['Sport'].isin(top_sports_brasil)]
    df_top_sports_brasil = df_top_sports[df_top_sports['NOC'] == 'BRA']
    # Analise da associacao entre os atributos fisicos e a medalha para cada esporte mais premiado do Brasil
    """for sport in top_sports_brasil:
        print(f'Analise do esporte: {sport}')
        df_filter_general = df_top_sports[df_top_sports['Sport'] == sport]
        df_filter_brasil = df_top_sports_brasil[df_top_sports_brasil['Sport'] == sport]
        for attribute in ['Age', 'Height', 'Weight']:
            print(f'---------------- \nAssociacao entre {attribute} e Medal - Geral')
            print(r2(df_filter_general, 'Medal', attribute, False))
            print(f'Associacao entre {attribute} e Medal - Brasil')
            print(r2(df_filter_brasil, 'Medal', attribute, False))

        print('\n\n')"""

    # Calculados os coeficientes r2 entre as medalhas e os atributos fisicos para cada esporte
    # Notamos que mal existe associacao entre tais atributos e a medalha ganha pelo atleta naquele esporte
    # Entre os jogadores brasileiros, existe uma associacao maior entre as variaveis, mas ainda e minimo
    # Vale somente ressaltar o volei, o futebol e o basquete brasileiros
    
    # Codigo para salvar os graficos da analise
    for sport in ['Volleyball', 'Football', 'Basketball']:
        df_sport_brasil = df_top_sports_brasil[df_top_sports_brasil['Sport'] == sport]
        for attribute in ['Height', 'Weight']:
            plt.figure()
            sns.boxplot(x='Medal', y=attribute, data=df_sport_brasil)
            plt.title(f'{sport} - {attribute}')
            plt.savefig(f'graphs/physical_attributes_graphs/{sport}_{attribute}.png')


def attributes_years_analysis(df: pd.DataFrame) -> None:
    """Função que recebe um DataFrame e analisa as possiveis relacoes de associacao entre suas variaveis de atributos fisicos com os anos.

    Args:
        df (pd.DataFrame): df dos atletas
    """
    # Analise da correlacao entre o ano e os atributos fisicos
    plt.xlabel('Year')
    for attribute in ['Age', 'Height', 'Weight']:
        plt.ylabel(attribute)
        
        df_brasil = df[df['NOC'] == 'BRA']
        #print(f'\n--------------- Correlacao entre {attribute} e Year - Geral')
        #print(corr(df, attribute, 'Year', False))
        plt.title(f'Correlacao: {attribute} e ano')
        plt.scatter(data=df, x='Year', y=attribute)
        
        plt.savefig(f'graphs/physical_attributes_graphs/{attribute}_ano.png')

        #print(f'\nCorrelacao entre {attribute} e Year - Brasil')
        #print(corr(df_brasil, attribute, 'Year', False))
        plt.title(f'Correlacao: {attribute} e ano')
        plt.scatter(data=df_brasil, x='Year', y=attribute)
        plt.savefig(f'graphs/physical_attributes_graphs/{attribute}_ano_brasil.png')

    # Idade parece se correlacionar mais com o Ano do que os demais atributos, mas ainda assim, muito pouco
    # No Brasil, pelo contrario, a idade quase nao variou, mas as correlacoes de altura e peso com o Ano sao mais significantes (ainda pouco) que a Idade
