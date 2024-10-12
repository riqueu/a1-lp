import unittest
import pandas as pd
from src.womens_participation import *
from src.womens_participation_graphs import *
from matplotlib import pyplot as plt

class TestCountAthletes(unittest.TestCase):
    
    def test_group_by_year_and_sex(self):
        # Teste com agrupamento por ['Year', 'Sex']
        data = {
            'Year': [2020, 2020, 2021, 2021, 2021],
            'Medal': [3, 2, 3, 1, 2],
            'Sex': ['F', 'M', 'F', 'M', 'F']
        }
        df = pd.DataFrame(data)

        # DataFrame esperado
        expected_data = {
            'Year': [2020, 2021],
            'F_Athletes': [1, 2],
            'M_Athletes': [1, 1],
            'Total_Athletes': [2, 3]
        }
        expected_df = pd.DataFrame(expected_data)
        result_df = count_athletes(df, 'Year', 'Sex')

        # Verifica se o DataFrame gerado é igual ao esperado
        self.assertTrue(result_df[['Year', 'F_Athletes', 'M_Athletes', 'Total_Athletes']].equals(expected_df))

    def test_group_by_country_and_sex(self):
        # Teste básico com agrupamento por '[NOC', 'Sex']
        data = {
            'Year': [2020, 2020, 2021, 2021],
            'NOC': ['BRA', 'BRA', 'USA', 'BRA'],
            'Medal': [0, 3, 2, 0],
            'Sex': ['F', 'M', 'F', 'M']
        }
        df = pd.DataFrame(data)

        # DataFrame esperado
        expected_data = {
            'NOC': ['BRA', 'USA'],
            'F_Athletes': [1, 1],
            'M_Athletes': [2, 0],
            'Total_Athletes': [3, 1]
        }
        expected_df = pd.DataFrame(expected_data)
        result_df = count_athletes(df, 'NOC', 'Sex')

        # Verifica se o DataFrame gerado é igual ao esperado
        self.assertTrue(result_df[['NOC', 'F_Athletes', 'M_Athletes', 'Total_Athletes']].equals(expected_df))

    def test_no_medals(self):
        # Teste com atletas que não ganharam medalhas 
        data = {
            'Year': [2020, 2020, 2021],
            'NOC': ['BRA', 'BRA', 'USA'],
            'Medal': [0, 0, 0],
            'Sex': ['F', 'M', 'F']
        }
        df = pd.DataFrame(data)

        # DataFrame esperado
        expected_data = {
            'NOC': ['BRA', 'USA'],
            'F_Athletes': [1, 1],
            'M_Athletes': [1, 0],
            'Total_Athletes': [2, 1]
        }
        expected_df = pd.DataFrame(expected_data)
        result_df = count_athletes(df, 'NOC', 'Sex')

        # Verifica se o DataFrame gerado é igual ao esperado
        self.assertTrue(result_df[['NOC', 'F_Athletes', 'M_Athletes', 'Total_Athletes']].equals(expected_df))

class TestUpdateMedalsOrScore(unittest.TestCase):
    
    def test_update_medals(self):
        # Cenário com agrpamento para contar medalhas por NOC e ano
        data = {
            'Medal': [0, 0, 0, 3, 0],
            'Year': [1992, 2012, 1920, 1900, 1988],
            'NOC': ['CHN', 'CHN', 'DEN', 'DEN', 'NED'],
            'Sex': ['M', 'M', 'M', 'M', 'F']
        }

        df = pd.DataFrame(data)

        # DataFrame esperado
        expected_data = {
            'Sex': [0,1,2,3,4],
            'Year': [1900, 1920, 1988, 1992, 2012],
            'NOC': ['DEN', 'DEN', 'NED', 'CHN', 'CHN'],
            'F_Medal': [0, 0, 0, 0, 0],
            'M_Medal': [1, 0, 0, 0, 0],
            'Total_Medal': [1, 0, 0, 0, 0]
        }
        

        expected_result = pd.DataFrame(expected_data)

        # Executa a função
        result_df = update_medals_or_score(df, 'Medal', *['Year', 'NOC', 'Sex'], **{'F': 'F_Medal', 'M': 'M_Medal'})
    
        
        self.assertEqual(result_df['M_Medal'].tolist(), expected_result['M_Medal'].tolist())
        self.assertEqual(result_df['F_Medal'].tolist(), expected_result['F_Medal'].tolist())
        self.assertEqual(result_df['NOC'].tolist(), expected_result['NOC'].tolist())
        self.assertEqual(result_df['Total_Medal'].tolist(), expected_result['Total_Medal'].tolist())
        self.assertEqual(result_df['Year'].tolist(), expected_result['Year'].tolist())
    
    
if __name__ == "__main__":
    unittest.main()