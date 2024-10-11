import pandas as pd
from src.data_predictor import *
import unittest


class TestToEncoded(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie', 'David'],
            'Age': [25, np.nan, 35, 40],
            'Gender': ['F', 'M', 'M', 'M'],
            'Height': [165, 175, np.nan, 180],
            'Weight': [55, 70, 80, np.nan],
            'Sport': ['Basketball', 'Soccer', 'Soccer', 'Basketball']
        })

    def test_to_encoded(self):
        df_encoded, cols_to_fix, cols_types, encoders = to_encoded(self.df)

        # Check if the dataframe is encoded correctly
        self.assertTrue('Gender' in encoders)
        self.assertTrue('Sport' in encoders)
        self.assertEqual(df_encoded['Gender'].tolist(), [0, 1, 1, 1])
        self.assertEqual(df_encoded['Sport'].tolist(), [0, 1, 1, 0])

        # Check if the columns to fix are identified correctly
        self.assertIn('Age', cols_to_fix)
        self.assertIn('Height', cols_to_fix)
        self.assertIn('Weight', cols_to_fix)

        # Check if the column types are identified correctly
        self.assertEqual(cols_types, {})

    def test_to_encoded_with_problematic_columns(self):
        df_problematic = self.df.copy()
        df_problematic['MixedType'] = [1, 'two', 3, 4]

        df_encoded, cols_to_fix, cols_types, encoders = to_encoded(df_problematic)

        # Check if the problematic column is identified correctly
        self.assertIn('MixedType', cols_to_fix)
        self.assertEqual(cols_to_fix['MixedType'], 'Contains two or more types')
        self.assertIn('MixedType', cols_types)

    def test_to_encoded_with_nan_columns(self):
        df_nan = self.df.copy()
        df_nan['AllNaN'] = [np.nan, np.nan, np.nan, np.nan]

        df_encoded, cols_to_fix, cols_types, encoders = to_encoded(df_nan)

        # Check if the column with all NaN values is identified correctly
        self.assertIn('AllNaN', cols_to_fix)
        self.assertEqual(cols_to_fix['AllNaN'], 'Contains NaN')


if __name__ == "__main__":
    unittest.main()