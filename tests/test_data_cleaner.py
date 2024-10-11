import pandas as pd
import numpy as np
from src.data_cleaner import *
import unittest # python -m unittest discover -s tests


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
        medals = modified_data['Medal']
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

            
class TestUrbanizationRenameCountries(unittest.TestCase):

    def test_urbanization_rename_countries_standard(self):
        data = pd.DataFrame({
            'Country': [
                "United States of America", "Côte d'Ivoire", "Korea, Republic of",
                "Korea, Dem. People's Rep. of", "Czechia", "Russian Federation",
                "United Kingdom", "Iran (Islamic Republic of)", "Netherlands (Kingdom of the)",
                "China, Taiwan Province of", "Trinidad and Tobago", "Türkiye",
                "Venezuela (Bolivarian Rep. of)", "Viet Nam"
            ]
        })
        expected_result = pd.DataFrame({
            'Country': [
                "USA", "Ivory Coast", "South Korea", "North Korea", "Czech Republic", "Russia",
                "UK", "Iran", "Netherlands", "Taiwan", "Trinidad", "Turkey",
                "Venezuela", "Vietnam"
            ]
        })
        modified_data = urbanization_rename_countries(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_urbanization_rename_countries_no_rename_needed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "Argentina", "Canada"]
        })
        expected_result = data.copy()
        modified_data = urbanization_rename_countries(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_urbanization_rename_countries_mixed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "United States of America", "Canada", "Türkiye"]
        })
        expected_result = pd.DataFrame({
            'Country': ["Brazil", "USA", "Canada", "Turkey"]
        })
        modified_data = urbanization_rename_countries(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_urbanization_rename_countries_missing_column(self):
        data = pd.DataFrame({
            'Nation': ["Brazil", "United States of America", "Canada"]
        })
        with self.assertRaises(SystemExit):
            urbanization_rename_countries(data)


class TestMapNameNormalization(unittest.TestCase):

    def test_map_name_normalization_standard(self):
        data = pd.DataFrame({
            'Country': ["USA", "UK", "Trinidad", "Macedonia", "Czech Republic", "Ivory Coast"]
        })
        expected_result = pd.DataFrame({
            'Country': [
                "United States of America", "United Kingdom", "Trinidad and Tobago",
                "North Macedonia", "Czechia", "Côte d'Ivoire"
            ]
        })
        modified_data = map_name_normalization(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_map_name_normalization_no_rename_needed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "Argentina", "Canada"]
        })
        expected_result = data.copy()
        modified_data = map_name_normalization(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_map_name_normalization_mixed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "USA", "Canada", "UK"]
        })
        expected_result = pd.DataFrame({
            'Country': ["Brazil", "United States of America", "Canada", "United Kingdom"]
        })
        modified_data = map_name_normalization(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_map_name_normalization_missing_column(self):
        data = pd.DataFrame({
            'Nation': ["Brazil", "USA", "Canada"]
        })
        with self.assertRaises(SystemExit):
            map_name_normalization(data)


class TestTransformAthletesDfToParalympicsFormat(unittest.TestCase):

    def test_transform_athletes_df_to_paralympics_format_standard(self):
        data = pd.DataFrame({
            'NOC': ['BRA', 'BRA', 'USA', 'USA', 'USA'],
            'Year': [2016, 2016, 2016, 2016, 2016],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Summer'],
            'Medal': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver'],
            'Sex': ['M', 'F', 'M', 'M', 'F']
        })
        expected_result = pd.DataFrame({
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Season': ['Summer', 'Summer'],
            'Gold': [1, 1],
            'Silver': [1, 1],
            'Bronze': [0, 1],
            'Men': [1, 2],
            'Women': [1, 1],
            'M_Total': [2, 3],
            'P_Total': [2, 3]
        })
        transformed_data = convert_athletes_df_to_paralympics_format(data)
        pd.testing.assert_frame_equal(expected_result, transformed_data)

    def test_convert_athletes_df_to_paralympics_format_no_medals(self):
        data = pd.DataFrame({
            'NOC': ['BRA', 'BRA', 'USA', 'USA'],
            'Year': [2016, 2016, 2016, 2016],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer'],
            'Medal': [None, None, None, None],
            'Sex': ['M', 'F', 'M', 'F']
        })
        expected_result = pd.DataFrame({
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Season': ['Summer', 'Summer'],
            'Gold': [0, 0],
            'Silver': [0, 0],
            'Bronze': [0, 0],
            'Men': [1, 1],
            'Women': [1, 1],
            'M_Total': [0, 0],
            'P_Total': [2, 2]
        })
        transformed_data = convert_athletes_df_to_paralympics_format(data)
        pd.testing.assert_frame_equal(expected_result, transformed_data)

    def test_convert_athletes_df_to_paralympics_format_mixed_years(self):
        data = pd.DataFrame({
            'NOC': ['BRA', 'BRA', 'USA', 'USA', 'USA'],
            'Year': [2016, 2012, 2016, 2012, 2016],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Summer'],
            'Medal': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver'],
            'Sex': ['M', 'F', 'M', 'M', 'F']
        })
        expected_result = pd.DataFrame({
                'NOC': ['BRA', 'BRA', 'USA', 'USA'],
                'Year': [2012, 2016, 2012, 2016],
                'Season': ['Summer', 'Summer', 'Summer', 'Summer'],
                'Gold': [0, 1, 1, 0],
                'Silver': [1, 0, 0, 1],
                'Bronze': [0, 0, 0, 1],
                'Men': [0, 1, 1, 1],
                'Women': [1, 0, 0, 1],
                'M_Total': [1, 1, 1, 2],
                'P_Total': [1, 1, 1, 2]
        })
        transformed_data = convert_athletes_df_to_paralympics_format(data)
        pd.testing.assert_frame_equal(expected_result, transformed_data)

    def test_convert_athletes_df_to_paralympics_format_missing_columns(self):
        data = pd.DataFrame({
            'NOC': ['BRA', 'BRA', 'USA', 'USA'],
            'Year': [2016, 2016, 2016, 2016],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer'],
            'Sex': ['M', 'F', 'M', 'F']
        })
        with self.assertRaises(KeyError):
            convert_athletes_df_to_paralympics_format(data)


class TestAggregateMedalsByEventTeam(unittest.TestCase):

    def test_aggregate_medals_by_event_team_standard(self):
        data = pd.DataFrame({
            'Event': ['100m', '100m', '100m', '200m', '200m'],
            'Team': ['Brazil', 'Brazil', 'Brazil', 'USA', 'USA'],
            'NOC': ['BRA', 'BRA', 'BRA', 'USA', 'USA'],
            'Year': [2016, 2016, 2016, 2016, 2016],
            'Games': ['2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Summer'],
            'City': ['Rio', 'Rio', 'Rio', 'Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics', 'Athletics', 'Athletics', 'Athletics'],
            'Medal': ['Gold', 'Gold', 'Gold', 'Silver', 'Silver']
        })
        expected_result = pd.DataFrame({
            'Event': ['100m', '200m'],
            'Team': ['Brazil', 'USA'],
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Games': ['2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer'],
            'City': ['Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics'],
            'Medal': ['Gold', 'Silver']
        })
        aggregated_data = aggregate_medals_by_event_team(data)
        pd.testing.assert_frame_equal(expected_result, aggregated_data)

    def test_aggregate_medals_by_event_team_no_medals(self):
        data = pd.DataFrame({
            'Event': ['100m', '200m'],
            'Team': ['Brazil', 'USA'],
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Games': ['2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer'],
            'City': ['Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics'],
            'Medal': [None, None]
        })
        expected_result = pd.DataFrame({
            'Event': ['100m', '200m'],
            'Team': ['Brazil', 'USA'],
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Games': ['2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer'],
            'City': ['Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics'],
            'Medal': [None, None]
        })
        aggregated_data = aggregate_medals_by_event_team(data)
        pd.testing.assert_frame_equal(expected_result, aggregated_data)

    def test_aggregate_medals_by_event_team_mixed_medals(self):
        data = pd.DataFrame({
            'Event': ['100m', '100m', '200m', '200m', '200m'],
            'Team': ['Brazil', 'Brazil', 'USA', 'USA', 'USA'],
            'NOC': ['BRA', 'BRA', 'USA', 'USA', 'USA'],
            'Year': [2016, 2016, 2016, 2016, 2016],
            'Games': ['2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Summer'],
            'City': ['Rio', 'Rio', 'Rio', 'Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics', 'Athletics', 'Athletics', 'Athletics'],
            'Medal': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver']
        })
        expected_result = pd.DataFrame({
            'Event': ['100m', '200m'],
            'Team': ['Brazil', 'USA'],
            'NOC': ['BRA', 'USA'],
            'Year': [2016, 2016],
            'Games': ['2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer'],
            'City': ['Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics'],
            'Medal': ['Gold', 'Bronze']
        })
        aggregated_data = aggregate_medals_by_event_team(data)
        pd.testing.assert_frame_equal(expected_result, aggregated_data)

    def test_aggregate_medals_by_event_team_missing_columns(self):
        data = pd.DataFrame({
            'Event': ['100m', '200m'],
            'Team': ['Brazil', 'USA'],
            'Year': [2016, 2016],
            'Games': ['2016 Summer', '2016 Summer'],
            'Season': ['Summer', 'Summer'],
            'City': ['Rio', 'Rio'],
            'Sport': ['Athletics', 'Athletics'],
            'Medal': ['Gold', 'Silver']
        })
        with self.assertRaises(KeyError):
            aggregate_medals_by_event_team(data)


class TestRenameCountriesGDP(unittest.TestCase):

    def test_rename_countries_gdp_standard(self):
        data = pd.DataFrame({
            'Country': [
                "Bahamas, The", "Curacao", "Iran, Islamic Rep.", "Russian Federation",
                "Korea, Rep.", "Syrian Arab Republic", "Trinidad and Tobago",
                "United Kingdom", "United States", "Venezuela, RB"
            ]
        })
        expected_result = pd.DataFrame({
            'Country': [
                "Bahamas", "Curacao", "Iran", "Russia", "South Korea", "Syria",
                "Trinidad", "UK", "USA", "Venezuela"
            ]
        })
        modified_data = rename_countries_gdp(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_rename_countries_gdp_no_rename_needed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "Argentina", "Canada"]
        })
        expected_result = data.copy()
        modified_data = rename_countries_gdp(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_rename_countries_gdp_mixed(self):
        data = pd.DataFrame({
            'Country': ["Brazil", "Bahamas, The", "Canada", "Iran, Islamic Rep."]
        })
        expected_result = pd.DataFrame({
            'Country': ["Brazil", "Bahamas", "Canada", "Iran"]
        })
        modified_data = rename_countries_gdp(data)
        self.assertEqual(expected_result['Country'].tolist(), modified_data['Country'].tolist())

    def test_rename_countries_gdp_missing_column(self):
        data = pd.DataFrame({
            'Nation': ["Brazil", "Bahamas, The", "Canada"]
        })
        with self.assertRaises(SystemExit):
            rename_countries_gdp(data)


if __name__ == "__main__":
    unittest.main()