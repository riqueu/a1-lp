"""Modulo com as funcoes para a hipotese do perfil fisico dos atletas"""
import numpy as pd
import pandas as pd
from data_cleaner import medals_to_int
from data_predictor import *
from coeficient_functions import r2


original = pd.read_csv('athlete_events.csv')
df = pd.read_csv('inverse.csv', index_col=0)

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


# Classificacao dos esportes nas 7 categorias
df['sport_class'] = df['Sport'].map(sport_map)


# Filtro para os esportes mais coerentes
coerente = original[['Sport', 'Sex', 'Age', 'Height', 'Weight']].groupby('Sport').count()
coerente['complete'] = coerente.apply(lambda x: x.sum()/(x.shape[0]*x.Sex), axis=1)
coerente = coerente.reset_index().sort_values(by='complete', ascending=False).set_index('Sport')
sports_complete_map = coerente['complete'].to_dict()
df['complete'] = df['Sport'].map(sports_complete_map)
df = df.sort_values(by='complete', ascending=False)
top_sports_complete = list(sports_complete_map.keys())[:7]


# Filtro para pegar os esporte mais coerente de cada categoria
category = df.groupby('sport_class').first().reset_index()
top_sports_complete_category = category.Sport.unique()


# Filtro para os esportes mais premiados do Brasil
df_brasil = df[df['NOC'] == 'BRA']
df_medals_brasil = df_brasil[['Sport', 'Medal', 'Sex', 'Age', 'Height', 'Weight']].groupby('Sport').count()
df_medals_brasil = df_medals_brasil.reset_index().sort_values(by='Medal', ascending=False)
top_sports_brasil = df_medals_brasil.head(7).Sport


# df, cols_to_fix, cols_types, encoders = to_encoded(df)
# print(f'Colunas problematicas: {cols_to_fix}\nColunas com varios tipos: {cols_types}')


# Verificacao das associacoes dos atributos fisicos com as colunas de esporte (geral ou categorizado) para cada filtro
for filter_sport, name_filter in zip([top_sports_complete, top_sports_complete_category, top_sports_brasil], ['Top_complete', 'Top_complete_category', 'brasil']):
    print(f'Analisando o filtro: {name_filter}\n')
    df_filter = df[df['Sport'].isin(filter_sport)]
    for column_quali in ['Sport', 'sport_class']:
        print(f'--------------- Analisando associacao com {column_quali}:')
        for attribute in ['Age', 'Height', 'Weight']:
            r_2 = r2(df_filter, column_quali, attribute, False)
            print(f'Associacao entre {column_quali} e {attribute}')
            print(f'Coeficiente r_2 = {r_2}\n')
    print('\n\n\n')


# E evidente que a os atributos fisicos estao mais associados ao proprio esporte do que a categoria dele
# Idade e geralmente o atributo que tem menor associacao com o esporte
# Para os esportes mais premiados do Brasil, os atributos parecem tem maior associacao com o esporte do que quando aplicado a outros esportes