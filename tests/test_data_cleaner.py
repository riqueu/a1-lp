import pandas as pd
import numpy as np
from src.data_cleaner import *
import unittest

            
class TestMedalsToInt(unittest.TestCase):
    
    # Test the function with a dataframe with all types of medals present.
    def test_all_types_of_medals_present(self):
        
        data = pd.DataFrame({
        'Name': ['Alice', 'Bryan', 'Carlos', 'Daniel', 'Eliel'], 
        'Medal': ['Gold', 'Silver', 'Bronze', np.nan, 'Gold'], 
        'Height':  [170, 160, 150, 155, 187], 
        'Weight': [80, 60, 65, 46, 89], 
        'Age': [15, 16, 17, 18, 19]
})
        modified_data = medals_to_int(data)
        medals = modified_data['Medal']
        expected_result =  [3, 2, 1, 0, 3]
        
        self.assertEqual(expected_result, medals.tolist())
        
    
    # Test the function with a dataframe without medals
    def test_without_medals(self):
        
        data = pd.DataFrame({
        'Name': ['Gustavo', 'Luciano', 'Chappel', 'Ariana', 'Taylor'], 
        'Medal': [np.nan, np.nan, np.nan, np.nan, np.nan], 
        'Height': [170, 160, 150, 155, 187], 
         'Weight': [80, 60, 65, 46, 89], 
        'Age': [15, 16, 17, 18, 19]
})
        modified_data = medals_to_int(data)
        medals = data['Medal']
        expected_result = [0, 0, 0, 0, 0]
        self.assertEqual(expected_result, medals.tolist())


     # Test the function with a dataframe that doesn't have the Medals column 
    def test_without_medal_column(self):
        data = pd.DataFrame({
        'Atleta': ['Jaime', 'Willian', 'Carneiro'], 
        'Height': [170, 160, 150], 
         'Weight': [80, 60, 65], 
        'Age': [15, 16, 17]
})
        
        with self.assertRaises(SystemExit):
            medals_to_int(data)
            
class TestPredictMissing(unittest.TestCase):
    # TODO
    #  Adicionar mais casos de teste
    
    #  Test the function with a  DataFrame with one only 
    def test_a_full_row_only(self):
        
        data = data = pd.DataFrame({
    'Sport': ['Soccer', 'Soccer', 'Soccer'],
    'Sex': ['F', 'F', 'F'],
    'Age': [25, np.nan, 22],
    'Height': [160, 165, np.nan],
    'Weight': [55, np.nan, 60]
})
        expected_result = data = pd.DataFrame({
    'Sport': ['Soccer', 'Soccer', 'Soccer'],
    'Sex': ['F', 'F', 'F'],
    'Age': [25, 25, 22],
    'Height': [160, 165, 160],
    'Weight': [55, 55, 60]
})      
        
        modified_data = predict_missing(data) 
        
        self.assertEqual(expected_result['Age'].tolist(), modified_data['Age'].tolist())
        self.assertEqual(expected_result['Height'].tolist(), modified_data['Height'].tolist())
        self.assertEqual(expected_result['Weight'].tolist(), modified_data['Weight'].tolist())
        
        """
        Outra possibilidade:
        from pandas.testing import assert_frame_equal
        
        assert_frame_equal(df1, df2)
        """

    
    def test_no_missing_values(self):
        
        data = pd.DataFrame({
    'Sport': ['Tennis', 'Tennis', 'Tennis', 'Tennis'],
    'Sex': ['M', 'F', 'F', 'M'],
    'Age': [30, 25, 18, 19],
    'Height': [180, 170, 160, 155],
    'Weight': [75, 65, 68, 81]
})
        expected_result = data.copy()

        modified_data = predict_missing(data)
        
        self.assertEqual(expected_result['Age'].tolist(), modified_data['Age'].tolist())
        self.assertEqual(expected_result['Height'].tolist(), modified_data['Height'].tolist())
        self.assertEqual(expected_result['Weight'].tolist(), modified_data['Weight'].tolist())

class TestValidateAthletesColumns(unittest.TestCase):

    def test_all_columns_present(self):
        data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['Ana', 'Pedro', 'Maria'],
            'Sex': ['F', 'M', 'F'],
            'Age': [23, 35, 29],
            'Height': [160.0, 175.0, 165.0],
            'Weight': [55.0, 70.0, 60.0],
            'Team': ['Brazil', 'Brazil', 'Brazil'],
            'NOC': ['BRA', 'BRA', 'BRA'],
            'Games': ['2016 Summer', '2016 Summer', '2016 Summer'],
            'Year': [2016, 2016, 2016],
            'Season': ['Summer', 'Summer', 'Summer'],
            'City': ['Rio', 'Rio', 'Rio'],
            'Sport': ['Swimming', 'Football', 'Athletics'],
            'Event': ['200m Freestyle', 'Football', '100m Sprint'],
            'Medal': [None, 'Gold', None]
        })
        try:
            validade_athletes_columns(data)
        except KeyError:
            self.fail("validade_athletes_columns raised KeyError unexpectedly!")

    def test_missing_columns(self):
        data = pd.DataFrame({
            'ID': [1, 2, 3],
            'Name': ['Ana', 'Pedro', 'Maria'],
            'Sex': ['F', 'M', 'F'],
            'Age': [23, 35, 29]
            # Missing other required columns
        })
        with self.assertRaises(KeyError):
            validade_athletes_columns(data)

    def test_empty_dataframe(self):
        data = pd.DataFrame()
        with self.assertRaises(KeyError):
            validade_athletes_columns(data)

class TestRenameCountries(unittest.TestCase):
    # TODO
    # adicionar testes de caso
    pass
if __name__ == "__main__":
    unittest.main()