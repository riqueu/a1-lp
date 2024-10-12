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

        expected_data = {
            'NOC': ['BRA', 'USA'],
            'F_Athletes': [1, 1],
            'M_Athletes': [2, 0],
            'Total_Athletes': [3, 1]
        }
        expected_df = pd.DataFrame(expected_data)
        result_df = count_athletes(df, 'NOC', 'Sex')

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

class TestMergeByCountry(unittest.TestCase):

    def setUp(self):
        """Função que cria os DataFrames para usar nos testes."""
        self.df_main = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'NOC': ['USA', 'BRA', 'CHN'],
            'T_Medal': [40, 20, 30]
        })

        self.df_aux = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'NOC': ['USA', 'BRA', 'CHN'],
            'Athletes': [100, 80, 120]
        })

    def test_normal_merge(self):
        """Teste para verificar o merge com dados normais."""
        result = merge_by_country(self.df_main, self.df_aux)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'NOC': ['USA', 'BRA', 'CHN'],
            'T_Medal': [40, 20, 30],
            'Athletes': [100, 80, 120]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_missing_values(self):
        """Teste para verificar se o merge lida corretamente com valores faltantes."""
        df_aux_with_missing = pd.DataFrame({
            'Year': [2000, 2008],
            'NOC': ['USA', 'CHN'],
            'Athletes': [100, 120]
        })

        result = merge_by_country(self.df_main, df_aux_with_missing)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'NOC': ['USA', 'BRA', 'CHN'],
            'T_Medal': [40, 20, 30],
            'Athletes': [100, None, 120]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_empty_dataframes(self):
        """Teste para verificar se a função lida com dataframes vazios."""
        df_empty = pd.DataFrame(columns=['Year', 'NOC', 'Athletes'])
        result = merge_by_country(self.df_main, df_empty)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'NOC': ['USA', 'BRA', 'CHN'],
            'T_Medal': [40, 20, 30],
            'Athletes': [None, None, None]
        })

        pd.testing.assert_frame_equal(result, expected)

class TestMergeByYear(unittest.TestCase):

    def setUp(self):
        """Função que cria os DataFrames para usar nos testes."""
        self.df_main = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'T_Medal': [40, 20, 30]
        })

        self.df_aux = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Athletes': [100, 80, 120]
        })

    def test_normal_merge(self):
        """Teste para verificar o merge com dados normais."""
        result = merge_by_year(self.df_main, self.df_aux)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'T_Medal': [40, 20, 30],
            'Athletes': [100, 80, 120]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_missing_values(self):
        """Teste para verificar o comportamento com valores faltantes."""
        df_aux_with_missing = pd.DataFrame({
            'Year': [2000, 2008],
            'Athletes': [100, 120]
        })

        result = merge_by_year(self.df_main, df_aux_with_missing)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'T_Medal': [40, 20, 30],
            'Athletes': [100, None, 120]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_empty_dataframes(self):
        """Teste para verificar se a função lida com dataframes vazios."""
        df_empty = pd.DataFrame(columns=['Year', 'Athletes'])
        result = merge_by_year(self.df_main, df_empty)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'T_Medal': [40, 20, 30],
            'Athletes': [None, None, None]
        })

        pd.testing.assert_frame_equal(result, expected)
    
class TestMergeBySport(unittest.TestCase):

    def setUp(self):
        """Função que cria os DataFrames para usar nos testes."""
        self.df_main = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Sport': ['Football', 'Basketball', 'Swimming'],
            'T_Medal': [10, 15, 20]
        })

        self.df_aux = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Sport': ['Football', 'Basketball', 'Swimming'],
            'Athletes': [50, 30, 60]
        })

    def test_normal_merge(self):
        """Teste para verificar o merge com dados normais."""
        result = merge_by_sport(self.df_main, self.df_aux)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Sport': ['Football', 'Basketball', 'Swimming'],
            'T_Medal': [10, 15, 20],
            'Athletes': [50, 30, 60]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_missing_values(self):
        """Teste para verificar o comportamento com valores faltantes."""
        df_aux_with_missing = pd.DataFrame({
            'Year': [2000, 2008],
            'Sport': ['Football', 'Swimming'],
            'Athletes': [50, 60]
        })

        result = merge_by_sport(self.df_main, df_aux_with_missing)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Sport': ['Football', 'Basketball', 'Swimming'],
            'T_Medal': [10, 15, 20],
            'Athletes': [50, None, 60]
        })

        pd.testing.assert_frame_equal(result, expected)

    def test_empty_dataframes(self):
        """Teste para verificar se a função lida com dataframes vazios."""
        df_empty = pd.DataFrame(columns=['Year', 'Sport', 'Athletes'])
        result = merge_by_sport(self.df_main, df_empty)

        expected = pd.DataFrame({
            'Year': [2000, 2004, 2008],
            'Sport': ['Football', 'Basketball', 'Swimming'],
            'T_Medal': [10, 15, 20],
            'Athletes': [None, None, None]
        })

        pd.testing.assert_frame_equal(result, expected)

class TestEstimateStatistics(unittest.TestCase):

    def setUp(self):
        """Função que cria um DataFrame para usar nos testes."""
        self.df = pd.DataFrame({
            'F_Athletes': [10, -5, 15, 0, 20],
            'F_Medal': [2, 3, 4, -1, 5],
            'F_Score': [90, 85, 88, 0, 92],
            'Other_Column': [1, 2, 3, 4, 5] 
        })

    def test_statistics_with_and_without_outliers(self):
        """Teste para verificar as estatísticas antes e depois de remover outliers."""
        result = estimate_statistics(self.df)

        # Checa se o resultado tem 2 vezes o número de linhas do describe (um antes e um depois dos outliers)
        self.assertEqual(result.shape[0], 16) 

        # Verifica se as estatísticas para as colunas específicas estão corretas
        df_with_outliers = self.df[['F_Athletes', 'F_Medal', 'F_Score']].describe()
        df_without_outliers = self.df[(self.df['F_Athletes'] > 0) & (self.df['F_Medal'] > 0) & (self.df['F_Score'] > 0)][['F_Athletes', 'F_Medal', 'F_Score']].describe()

        expected_result = pd.concat([df_with_outliers, df_without_outliers])

        pd.testing.assert_frame_equal(result, expected_result)

    def test_empty_dataframe(self):
        """Teste para verificar o comportamento com um DataFrame vazio."""
        df_empty = pd.DataFrame(columns=['F_Athletes', 'F_Medal', 'F_Score'])
        result = estimate_statistics(df_empty)

        # Describe de um DataFrame vazio
        expected = pd.concat([df_empty.describe(), df_empty.describe()])

        pd.testing.assert_frame_equal(result, expected)

    def test_no_outliers(self):
        """Teste para verificar o comportamento quando não há outliers (valores negativos ou zero)."""
        df_no_outliers = pd.DataFrame({
            'F_Athletes': [10, 15, 20],
            'F_Medal': [2, 3, 4],
            'F_Score': [90, 85, 88]
        })

        result = estimate_statistics(df_no_outliers)

        df_describe = df_no_outliers[['F_Athletes', 'F_Medal', 'F_Score']].describe()
        expected = pd.concat([df_describe, df_describe])

        pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()