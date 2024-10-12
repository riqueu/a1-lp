import unittest
import pandas as pd
from src.olympics_paralympics_pib_analysis import *
from matplotlib import pyplot as plt


class TestAddCountryFromNoc(unittest.TestCase):
    # Configura os DataFrames para os testes
    def setUp(self):
        
        self.paralympics_df = pd.DataFrame({
            'Year': [2020, 2020, 2020],
            'NOC': ['USA', 'CAN', 'GBR'],
            'Season': ['Summer', 'Summer', 'Summer'],
            'Gold': [10, 5, 8],
            'Silver': [5, 3, 4],
            'Bronze': [2, 1, 2],
            'M_Total': [17, 9, 14],
            'Men': [10, 5, 6],
            'Women': [7, 4, 8],
            'P_Total': [17, 9, 14]
        })

        self.noc_df = pd.DataFrame({
            'NOC': ['USA', 'CAN', 'GBR', 'AUS'],
            'Country': ['United States', 'Canada', 'Great Britain', 'Australia']
        })

    # Teste para verificar se a coluna 'Country' é adicionada corretamente      
    def test_add_country_success(self):
        result = add_country_from_noc(self.paralympics_df, self.noc_df)
        expected = pd.DataFrame({
            'Year': [2020, 2020, 2020],
            'Country': ['United States', 'Canada', 'Great Britain'],
            'NOC': ['USA', 'CAN', 'GBR'],
            'Season': ['Summer', 'Summer', 'Summer'],
            'Gold': [10, 5, 8],
            'Silver': [5, 3, 4],
            'Bronze': [2, 1, 2],
            'M_Total': [17, 9, 14],
            'Men': [10, 5, 6],
            'Women': [7, 4, 8],
            'P_Total': [17, 9, 14]
        })
        pd.testing.assert_frame_equal(result, expected)

    # Teste para verificar se um KeyError é lançado quando a coluna 'NOC' está ausente  
    def test_missing_noc_column(self):
        missing_noc_df = self.paralympics_df.drop(columns=['NOC'])
        with self.assertRaises(KeyError):
            add_country_from_noc(missing_noc_df, self.noc_df)

    # Teste para verificar se uma exceção é lançada quando a mesclagem falha
    def test_merge_error(self):
        
        invalid_noc_df = pd.DataFrame({
            'NOC': ['USA', 'CAN', 'XYZ'],
            'Country': ['United States', 'Canada', 'Unknown']
        })
        result = add_country_from_noc(self.paralympics_df, invalid_noc_df)
        expected = pd.DataFrame({
            'Year': [2020, 2020, 2020],
            'Country': ['United States', 'Canada', None],  # GBR não existe em invalid_noc_df
            'NOC': ['USA', 'CAN', 'GBR'],
            'Season': ['Summer', 'Summer', 'Summer'],
            'Gold': [10, 5, 8],
            'Silver': [5, 3, 4],
            'Bronze': [2, 1, 2],
            'M_Total': [17, 9, 14],
            'Men': [10, 5, 6],
            'Women': [7, 4, 8],
            'P_Total': [17, 9, 14]
        })
        pd.testing.assert_frame_equal(result, expected)
   

class TestPivotGdpToLong(unittest.TestCase):

    def setUp(self):
        # Exemplo de DataFrame no formato wide
        self.gdp_df_wide = pd.DataFrame({
            'Country Name': ['Country A', 'Country B'],
            '2000': [1000, 2000],
            '2001': [1100, 2100],
            '2002': [1200, 2200]
        })

        # DataFrame esperado no formato long
        self.gdp_df_long_expected = pd.DataFrame({
            'Year': [2000, 2000, 2001, 2001, 2002, 2002],
            'Country': ['Country A', 'Country B', 'Country A', 'Country B', 'Country A', 'Country B'],
            'GDP': [1000, 2000, 1100, 2100, 1200, 2200]
        })

    def test_transform_wide_to_long(self):
        result = pivot_gdp_to_long(self.gdp_df_wide)
        
        # Verificar coluna por coluna
        for col in self.gdp_df_long_expected.columns:
            with self.subTest(col=col):
                # Converte a coluna Year para int64
                if col == 'Year':
                    pd.testing.assert_series_equal(result[col].reset_index(drop=True).astype('int64'), 
                                                    self.gdp_df_long_expected[col].reset_index(drop=True))
                else:
                    pd.testing.assert_series_equal(result[col].reset_index(drop=True), 
                                                    self.gdp_df_long_expected[col].reset_index(drop=True))

    # Testa o caso em que a coluna 'Country Name' está ausente
    def test_missing_country_name_column(self):
        
        gdp_df_missing_column = self.gdp_df_wide.drop(columns=['Country Name'])
        with self.assertRaises(KeyError):
            pivot_gdp_to_long(gdp_df_missing_column)

    
if __name__ == "__main__":
    unittest.main()