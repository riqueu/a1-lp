import pandas as pd
from src.coeficient_functions import *
import numpy as np
import unittest

class TestR2(unittest.TestCase):
    
    #  Teste com um dataframe valido e  esperado
    def test_with_a_valid_and_expected_dataframe(self):
        
        df = pd.DataFrame({
            'qualitativa': ['A', 'A', 'B', 'B', 'C', 'C'],
            'quantitativa': [1, 2, 3, 4, 5, 6]
        })

        
        expected_r2 = 0.8571428571428571  # Valor esperado
        
        self.assertAlmostEqual(r2(df, 'qualitativa', 'quantitativa'), expected_r2)
    
    
    # Teste para verificar se a função levanta um ValueError com valores inválidos
    def test_r2_invalid_values(self):
            
        # with self.assertRaises(ValueError) as context:
        #         r2(self.df_invalid_values, 'qualitativa', 'quantitativa')
        #         self.assertEqual(str(context.exception), 'Quanti column has non-numeric values')
        
        data = pd.DataFrame({
            'qualitativa': ['P', 'Q', 'R'],
            'quantitativa': [1, 2, 'invalid']
        })
        
        with self.assertRaises(ValueError) as context:
             r2(data, 'qualitativa', 'quantitativa')
    

    # Teste com o argumento is_sample como False
    def test_r2_sample_argument(self):
        
        df_sample = pd.DataFrame({
            'qualitativa': ['A', 'B', 'A', 'B'],
            'quantitativa': [1, 2, 3, 4]
        })
        expected_r2 = 0.20000000000000018  
        self.assertAlmostEqual(r2(df_sample, 'qualitativa', 'quantitativa', is_sample=False), expected_r2)

    # Teste com a coluna 'quali' ausente 
    def test_missing_quali_column(self):
        
        df = pd.DataFrame({
            'quantitativa': [1, 2, 3]
        })
        
        with self.assertRaises(KeyError) as context:
             r2(df, 'qualitativa', 'quantitativa')
    
    def test_missing_quanti_column(self):
        
        df = pd.DataFrame({
            'qualitativa': ['S', 'T', 'U']
        })
        
        with self.assertRaises(KeyError) as context:
             r2(df, 'qualitativa', 'quantitativa')

c