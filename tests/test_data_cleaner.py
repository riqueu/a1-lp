import pandas as pd
import numpy as np
from src.data_cleaner import *

import unittest

class TestMedalsToInt(unittest.TestCase):
    
    # Test the function with a dataframe with all types of medals present.
    def test_all_types_of_medals_present(self):
        
        data = pd.DataFrame({
        'Atleta': ['A', 'B', 'C', 'D', 'E'], 
        'Medal': ['Gold', 'Silver', 'Bronze', np.nan, 'Gold']
})
        standardized_data = medals_to_int(data)
        medals = standardized_data['Medal']
        expected_result =  [3, 2, 1, 0, 3]
        
        self.assertEqual(expected_result, medals.tolist())
        
    
    # Test the function with a dataframe without medals
    def test_without_medals(self):
        
        data = pd.DataFrame({
        'Atleta': ['Gustavo', 'Luciano', 'Chappel', 'Ariana', 'Taylor'], 
        'Medal': [np.nan, np.nan, np.nan, np.nan, np.nan], 
        'Height': [170, 160, 150, 155, 187]
})
        standardized_data = medals_to_int(data)
        medals = data['Medal']
        expected_result = [0, 0, 0, 0, 0]
        self.assertEqual(expected_result, medals.tolist())


     # Test the function with a dataframe that doesn't have the Medals column 
    def test_withou_medal_collumn(self):
        data = pd.DataFrame({
        'Atleta': ['Jaime', 'Willian', 'Carneiro']
})
        
        with self.assertRaises(SystemExit):
            medals_to_int(data)
            


if __name__== "__main__":
    unittest.main()
    
    
# df = pd.read_csv('data/athlete_events.csv')
# df = df[['Name', 'Sex', 'Age', 'Weight', 'Height', 'Sport']]
# # df= df.head(10000)
# # df_t = df[['Sport', 'Sex', 'Age']].groupby(['Sport', 'Sex']).count()
# # poucos_dados = df_t[df_t['Age'] == 1].reset_index()['Sport']
# # df = df[~df['Sport'].isin(poucos_dados)]
# # df_1 = predict_missing(df)
# # print(df_1)
# df_bktb = df[df['Sport']=="Basketball"]
# df_bktb = df_bktb[['Name', 'Sex', 'Age', 'Weight', 'Height', 'Sport']]


# print(len(df_bktb))
# df_tratado = predict_missing(df_bktb)
# print(df_tratado)
# print(len(df_tratado))

# print(len(df))

# df_tratado = predict_missing(df)
# print(df_tratado)
# print(len(df_tratado))
# # df_tratado= predict_missing(df)
# # print(len(df_tratado))

