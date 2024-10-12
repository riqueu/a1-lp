import unittest
import pandas as pd
from src.womens_participation import *
from src.womens_participation_graphs import *
from matplotlib import pyplot as plt

class CreateScatterplot:
    
    # Cria os gráficos de dispersão
    def test_create_scatterplot(self):
        df_example = pd.DataFrame ({
                'Year': [1976, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016],
                'NOC': ['BRA'] * 10,
                'F_Athletes': [2, 6, 12, 10, 19, 11, 22, 54, 68, 102],
                'M_Athletes': [21, 24, 47, 31, 41, 52, 72, 130, 110, 184],
                'Total_Athletes': [23, 30, 59, 41, 60, 63, 94, 184, 178, 286],
                'F_Medal': [0, 19, 10, 2, 6, 7, 13, 15, 4, 37],
                'M_Medal': [2, 9, 18, 5, 15, 36, 47, 53, 31, 103],
                'Total_Medal': [2, 28, 28, 7, 21, 43, 60, 68, 35, 140],
                'F_Score': [0, 41, 17, 6, 9, 18, 25, 21, 8, 57],
                'M_Score': [4, 18, 28, 7, 22, 53, 113, 116, 80, 186],
                'Total_Score': [4, 59, 45, 13, 31, 71, 138, 137, 88, 243]
            })
        
        plot = plot_scatter_graph(df_example, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Paralympic Score (Brazil)', 'Score')
        
        self.assertEqual(plot.__class__.__name__, "module")


if __name__ == "__main__":
    unittest.main()