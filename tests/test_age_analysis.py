import pandas as pd
from src.age_analysis import *
import numpy as np
import unittest

class TestStatisticsByAge(unittest.TestCase):
    
    # Teste com DataFrame vazio.
    def test_empty_dataframe(self):
        
        empty_df = pd.DataFrame(columns=['Sport', 'Age'])
        result = statistics_by_age(empty_df)
        self.assertEqual(result, {})  # Deve retornar um dicionário vazio

    # Teste com DataFrame que falta a coluna 'Age.    
    def test_missing_columns(self):

        df_missing_age = pd.DataFrame({
            'Sport': ['Soccer', 'Basketball'],
        })
        with self.assertRaises(SystemExit):
            medals_to_int(df_missing_age)

    # Teste com um único esporte.
    def test_single_sport(self):
        
        single_sport_df = pd.DataFrame({
            'Sport': ['Soccer', 'Soccer'],
            'Age': [20, 21]
        })
        expected_result = {
            'Soccer': {
                'mediana': 20.5,
                '1º quartil': 20.25,
                '3º quartil': 20.75,
                'minimo': 20,
                'maximo': 21,
                'media': 20.5,
                'desvio_padrao': 0.7071067811865476,
                'variancia': 0.5,
                'limite inferior': 20,
                'limite superior': 22
            }
        }
        result = statistics_by_age(single_sport_df)
        self.assertEqual(result, expected_result)
    
    #  teste com mais que um esporte
    def test_with_some__different_sports(self):
        df = pd.DataFrame({
            'Sport': ['Soccer', 'Basketball', 'Tennis', 'Soccer', 'Basketball', 'Tennis'],
            'Age': [20, 35, 25, 21, 45, 19]
        })
        
        expected_result = {
            'Basketball': {
                'mediana': 40.0,
                '1º quartil': 37.5,
                '3º quartil': 42.5,
                'minimo': 35,
                'maximo': 45,
                'media': 40.0,
                'desvio_padrao': 7.0710678118654755,
                'variancia': 50.0,
                'limite inferior': 30,
                'limite superior': 50
            },
            'Soccer': {
                'mediana': 20.5,
                '1º quartil': 20.25,
                '3º quartil': 20.75,
                'minimo': 20,
                'maximo': 21,
                'media': 20.5,
                'desvio_padrao': 0.7071067811865476,
                'variancia': 0.5,
                'limite inferior': 20,
                'limite superior': 22
            },
            'Tennis': {
                'mediana': 22.0,
                '1º quartil': 20.5,
                '3º quartil': 23.5,
                'minimo': 19,
                'maximo': 25,
                'media': 22.0,
                'desvio_padrao': 4.242640687119285,
                'variancia': 18.0,
                'limite inferior': 16,
                'limite superior': 28
            }
        }
        result = statistics_by_age(df)
        
        self.assertEqual(result, expected_result)

class HighestAgeAplitudeSports(unittest.TestCase):
    
    # Teste com algusn esportes diferentes
    def test_with_some_different_sports(self):
        df = pd.DataFrame({
    'Sport': ['Soccer']*10 + ['Basketball']*10 + ['Tennis']*10 + ['Swimming']*10 + ['Boxing']*10 + ['Volleyball']*10 + ['Golf']*10,
    'Age': [20, 22, 45, 23, 21, 60, 18, 27, 29, 24, # Soccer
            30, 32, 35, 45, 38, 55, 19, 25, 50, 21, # Basketball
            19, 20, 40, 60, 23, 25, 55, 28, 30, 26, # Tennis
            15, 28, 34, 35, 33, 18, 24, 22, 25, 45, # Swimming
            17, 55, 29, 30, 32, 36, 20, 31, 33, 27, # Boxing
            65, 70, 58, 55, 62, 64, 66, 67, 60, 59, # Golf
            23, 45, 25, 28, 26, 44, 29, 27, 48, 22] # Volleyball
})
        expected_result =    {'Boxing': 2, 'Soccer': 2, 'Tennis': 1}
        
        result = highest_age_aplitude_sports(df)
        
        self.assertEqual(result, expected_result)
    
    # Teste com DataFrame vazio.
    def test_empty_dataframe(self):
        
        df = pd.DataFrame({'Sport': [], 'Age': []})
        result = highest_age_aplitude_sports(df)    
        
        expected_result = {}
        
        self.assertEqual(result,expected_result)
    
    #  teste sem a coluna Age
    def test_without_column_age(self):
        df_missing_age =  pd.DataFrame({'Sport': ['Soccer', 'Basketball']})
        
        with self.assertRaises(SystemExit):
            highest_age_aplitude_sports(df_missing_age)
    
    #  Teste sem a coluna Sport
    def test_without_column_age(self):
        df_missing_sport =   pd.DataFrame({'Age': [18, 20, 22, 23, 25]})
        
        with self.assertRaises(SystemExit):
            highest_age_aplitude_sports(df_missing_sport)
    
    # teste com apenas uma modalidade de esporte
    def test_wiht_one_sport(self):
        df= pd.DataFrame({'Sport': ['Soccer']*5, 'Age': [10, 20, 25, 30, 35]})  # Nenhum valor extremo
        
        expected_result = {}
        
        self.assertEqual(expected_result, highest_age_aplitude_sports(df))
    
    #  Teste sem valores extremos
    def test_without_extreme_values(self):
        df  = pd.DataFrame({
        'Sport': ['Tennis']*5 + ['Swimming']*5,
        'Age': [18, 20, 22, 21, 19, 23, 25, 24, 22, 23]  # Nenhum valor extremo
    })  
        expected_result = {}
        
        self.assertEqual(expected_result, highest_age_aplitude_sports(df))
        


class CreateBoxplotSportWithTheMosOutliers:
    
    #  Cria um boxplot de idade  com o espote com mais valores outliers
    def test_create_boxplot(self):
        data = pd.DataFrame({
       'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 
        'Medal': ['Gold', 'Gold', 'Silver', 'Bronze', np.nan], 
        'Age': [80, 20, 19, 19, 18], 
        'Sport': ['Volleybol', 'Volleybol', 'Volleybol', 'Volleybol', 'Volleybol']})       
        
        plot = create_boxplot_sport_with_the_most_outliers(data)
    
        self.assertEqual(plot.__class__.__name__, "module")

class CreateBoxplotTop3EsportesOutliers:
    
    #  Cria um boxplot de idade dos 3 esportes com mais outliers 
    def test_create_boxplot(self):
        data = pd.DataFrame({
       'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 
        'Medal': ['Gold', 'Gold', 'Silver', 'Bronze', np.nan], 
        'Age': [80, 20, 19, 19, 18], 
        'Sport': ['Volleybol', 'Volleybol', 'Volleybol', 'Volleybol', 'Volleybol']})       
        
        plot = create_boxplot_top_3_esportes_outliers(data)
    
        
        self.assertEqual(plot.__class__.__name__, "module")
    
class CreateBoxplotTop3EsportesMostAwarded:
    # Cria o box plot de idade dos 3 esportes mais premiados pelo Brasil
    def test_create_boxplot(self):
        df_example = pd.DataFrame({
            'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA', 'BRA', 'BRA', 'BRA'],
            'Sport': ['Soccer', 'Volleyball', 'Swimming', 'Swimming', 'Soccer', 'Soccer', 'Judo', 'Volleyball', 'Judo', 'Judo'],
            'Medal': [1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            'Age': [22, 24, 20, 23, 27, 26, 28, 25, 22, 24]
        })
        
        plot = create_boxplot_top_3_esportes_most_awarded(df_example)
        
        self.assertEqual(plot.__class__.__name__, "module")

class CreateBoxplotAgeAwardedAndNonAwardedAthletesInBrazil:
    # Cria o boxplot de idade dos atletas brasileiros categorizados entre premiados e não premiados
    def test_create_boxplot(self):
        df_example = pd.DataFrame({
         'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA', 'BRA'],
         'Medal': [1, 0, 1, 0, 1, 0, 1, 0],
         'Age': [22, 24, 20, 23, 27, 26, 28, 25]
     })
        plot = create_boxplot_age_awarded_and_non_awarded_athletes_in_brazil(df_example)
        
        self.assertEqual(plot.__class__.__name__, "module")

class CreateBoxplotAgeByMedalsAthletesInBrazil:
    
    #  Cria o boxplot de idade dos atletas brasileiros categorizado por tipo de medalha
    def test_create_boxplot(self):
        df_example = pd.DataFrame({
     'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA'],
         'Medal': ['3', '2', '1', 0, '3', '3', '2'],
         'Age': [22, 24, 20, 23, 27, 26, 28]
     })
        plot = create_boxplot_age_by_medals_athletes_in_brazil(df_example)
    
        self.assertEqual(plot.__class__.__name__, "module")     
        