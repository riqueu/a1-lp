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



if __name__ == "__main__":
    unittest.main()