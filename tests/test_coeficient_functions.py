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


class TestCorr(unittest.TestCase):
    
    #  Teste correlação igual a 1
    def test_perfect_positive_correlation(self):
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 6, 8, 10]})
        result = corr(df, 'x', 'y')
        expected = 1.0
       
        self.assertAlmostEqual(result, expected)
    
    #  Teste correlação igual a -1
    def test_perfect_negative_correlation(self):
        df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [5, 4, 3, 2, 1]})
        result = corr(df, 'a', 'b')
        expected = -1.0
        
        self.assertAlmostEqual(result, expected)
    
    #  Teste correlação igual a 0
    def test_no_correlation(self):
        df = pd.DataFrame({'m': [1, 2, 3, 4, 5], 'n': [7, 6, 5, 6, 7]})
        result = corr(df, 'm', 'n')
        expected = 0
        
        self.assertAlmostEqual(result, expected, places=1)

    #  Teste correlação amostral e populacional iguais
    def test_sample_vs_population(self):
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [5, 6, 7, 8, 9]})
        sample_corr = corr(df, 'x', 'y', is_sample=True)
        population_corr = corr(df, 'x', 'y', is_sample=False)
       
        self.assertAlmostEqual(sample_corr, population_corr, places=2)
    
    #  Teste com coluna ausente
    def test_non_existent_columns(self):
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [5, 6, 7, 8, 9]})
        with self.assertRaises(KeyError):
            corr(df, 'x', 'z')


if __name__ == "__main__":
    unittest.main()
