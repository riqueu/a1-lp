import unittest
import pandas as pd
from src.medalist_x_urbanization_analysis import *
from matplotlib import pyplot as plt


class TestMedalistUrbanizationAnalysis(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.athletes_df = pd.DataFrame({
            'Year': [2016, 2016, 2016, 2016],
            'NOC': ['USA', 'BRA', 'USA', 'BRA'],
            'Medal': [1, 2, 0, 3]
        })
        self.urbanization_df = pd.DataFrame({
            'Country': ['United States', 'Brazil'],
            'Year': [2016, 2016],
            'Pop_Absolute': [320000, 200000],
            'Urban_Pop_Percent': [81.6, 84.3]
        })
        self.noc_df = pd.DataFrame({
            'NOC': ['USA', 'BRA'],
            'Country': ['United States', 'Brazil']
        })

    def test_prepare_2016_medalist_urbanization_analysis(self):
        result = prepare_2016_medalist_urbanization_analysis(self.athletes_df, self.urbanization_df, self.noc_df)
        
        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        
        # Check if the DataFrame has the expected columns
        expected_columns = ['NOC', 'Medalists', 'Country', 'Pop_Absolute', 'Urban_Pop_Percent', 'Urban_Pop_Absolute', 'Urban_Medalist_Density']
        self.assertTrue(all(column in result.columns for column in expected_columns))
        
        # Check if the DataFrame has the correct number of rows
        self.assertEqual(len(result), 2)
        
        # Check if the values are calculated correctly
        usa_row = result[result['Country'] == 'United States'].iloc[0]
        self.assertEqual(usa_row['Medalists'], 1)
        self.assertAlmostEqual(usa_row['Urban_Pop_Absolute'], 261119999.99999997)
        self.assertAlmostEqual(usa_row['Urban_Medalist_Density'], 1 / (261119999.99999997))


class TestCreateScatterplot2016MedalistUrbanization(unittest.TestCase):

    def setUp(self):
        self.data_2016 = pd.DataFrame({
            'Country': ['United States', 'Brazil'],
            'Urban_Pop_Percent': [81.6, 84.3],
            'Urban_Medalist_Density': [0.000003, 0.000015],
            'Medalists': [1, 5]
        })

    def test_create_scatterplot_2016_medalist_urbanization(self):
        scatterplot = create_scatterplot_2016_medalist_urbanization(self.data_2016)
        
        # Check if the result is a matplotlib Axes object
        self.assertIsInstance(scatterplot, plt.Axes)


class TestPrepareMapVisualizationData(unittest.TestCase):

    def setUp(self):
        self.athletes_df = pd.DataFrame({
            'Year': [2016, 2012, 2008, 2004],
            'NOC': ['USA', 'BRA', 'USA', 'BRA'],
            'Medal': [1, 2, 0, 3],
            'Event': ['100m', '200m', '100m', '200m'],
            'Team': ['USA Team', 'BRA Team', 'USA Team', 'BRA Team'],
            'Games': ['2016 Summer', '2012 Summer', '2008 Summer', '2004 Summer'],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer'],
            'City': ['Rio de Janeiro', 'London', 'Beijing', 'Athens'],
            'Sport': ['Athletics', 'Athletics', 'Athletics', 'Athletics'],
        })
        self.urbanization_df = pd.DataFrame({
            'Country': ['United States', 'Brazil', 'United States', 'Brazil'],
            'Year': [2016, 2012, 2008, 2004],
            'Pop_Absolute': [320000, 200000, 310000, 190000],
            'Urban_Pop_Percent': [81.6, 84.3, 80.0, 83.0]
        })
        self.noc_df = pd.DataFrame({
            'NOC': ['USA', 'BRA'],
            'Country': ['United States', 'Brazil']
        })

    def test_prepare_map_visualization_data(self):
        result = prepare_map_visualization_data(self.athletes_df, self.urbanization_df, self.noc_df)
        
        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        
        # Check if the DataFrame has the expected columns
        expected_columns = ['Year', 'NOC', 'Medal', 'Country', 'Pop_Absolute', 'Urban_Pop_Percent']
        self.assertTrue(all(column in result.columns for column in expected_columns))


class TestCalculateDynamicGrowth(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'Country': ['United States', 'United States', 'Brazil', 'Brazil'],
            'Year': [2000, 2016, 2000, 2016],
            'Urban_Pop_Percent': [80.0, 81.6, 82.0, 84.3]
        })

    def test_calculate_dynamic_growth(self):
        result = calculate_dynamic_growth(self.data, 'Urban_Pop_Percent')
        
        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        
        # Check if the DataFrame has the expected columns
        expected_columns = ['Country', 'Urban_Pop_Percent_Dynamic_Growth']
        self.assertTrue(all(column in result.columns for column in expected_columns))


class TestCreateMapVisualization(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'Year': [2012, 2012, 2016, 2016],
            'NOC': ['CHN', 'BRA', 'CHN', 'BRA'],
            'Medal': [10, 5, 15, 20],
            'Country': ['China', 'Brazil', 'China', 'Brazil'],
            'Pop_Absolute': [320000, 200000, 310000, 190000],
            'Urban_Pop_Percent': [81.6, 84.3, 80.0, 83.0]
        })

    def test_create_map_visualization(self):
        map_visualization = create_map_visualization(self.data)
        
        # Check if the result is a matplotlib Figure object
        self.assertEqual(map_visualization.__class__.__name__, "module")


if __name__ == '__main__':
    unittest.main()
