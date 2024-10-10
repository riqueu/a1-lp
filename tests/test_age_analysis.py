import pandas as pd
from src.age_analysis import *
import matplotlib.pyplot as plt
import seaborn as sns 
import unittest

from src.data_cleaner import *
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
    def test_with_some_sports(self):
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
