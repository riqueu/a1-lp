"""Modulo com as funcoes para a hipotese do perfil fisico dos atletas"""
import numpy as pd
import pandas as pd
from data_cleaner import medals_to_int
from data_predictor import *
from coeficient_functions import r2

df = pd.read_csv('inverse.csv', index_col=0)

df, cols_to_fix, cols_types, encoders = to_encoded(df)
print(f'Colunas problematicas: {cols_to_fix}\nColunas com varios tipos: {cols_types}')

# Verificacao das colunas que tem maior correlacao com o esporte do atleta
for attribute in ['Year', 'Age', 'Height', 'Weight']:
    r_2 = r2(df, 'Sport', attribute)
    print(f'Correlacao entre \'Sport\' e \'{attribute}\'')
    print(f'Coeficiente r_2 = {r_2}\n')