"""Modulo com as funcoes para a hipotese do perfil fisico dos atletas"""
import numpy as pd
import pandas as pd
from data_cleaner import medals_to_int
from data_predictor import *

from sklearn.feature_selection import SelectKBest, chi2


df = pd.read_csv('inverse.csv', index_col=0)

df, cols_to_fix, cols_types, encoders = to_encoded(df)
print(f'Colunas problematicas: {cols_to_fix}\nColunas com varios tipos: {cols_types}')

# X = df.drop(['ID', 'Name', 'Sport'], axis=1)
# y = df.Sport

# sel = SelectKBest(chi2, k=4)
# selecionados = sel.fit_transform(X, y.astype(int))
# colunas = sel.get_feature_names_out()
# print(f'Aqui: {colunas}')


# Calculo do R2
def r2(df: pd.DataFrame, quali: str, quanti: str) -> int:
    """ Funcao que calcula o coeficiente R2, que quantifica a correlacao entre uma variavel qualitativa e um quantitativa

    Args:
        df (pd.DataFrame): Dataframe com todos os dados
        quali (str): Coluna com os valores da variavel qualitativa
        quanti (str): Coluna com os valores da variavel quantitativa

    Returns:
        int: Coeficiente R2
    """
    # As variaveis quanti e quali devem estar nas colunas do df
    columns = df.columns
    if np.isin(quanti, columns, invert=True) or np.isin(quali, columns, invert=True):
        raise KeyError('Quanti/Quali aren\'t on the columns')
    
    # A variavel quanti deve ter somente valores numericos
    if any(pd.to_numeric(df[quanti], errors='coerce').isna()):
        raise ValueError('Quanti column has non-numeric values')
    
    # Agrupa o dataframe pela coluna quali e calcula as medidas resumos para a variavel quanti em cada categoria quali
    df_quali_quanti = df[[quali, quanti]].groupby(quali).agg(
        {
            quanti: ['count', 'mean', 'std', 'max', 'min']
        }
    )
    df_quali_quanti.columns = ['qtd', 'mean', 'var', 'min', 'max']
    df_quali_quanti['var'] = df_quali_quanti['var'] ** 2
    
    # Calcula a variancia ponderada
    var_ponderada = df_quali_quanti['var'] * df_quali_quanti['qtd']
    var_ponderada = var_ponderada.sum() / df_quali_quanti['qtd'].sum()
    
    # Calcula a variancia geral
    var_geral = df[quanti].std()
    var_geral **= 2
    
    # Calcula o R2
    r2 = 1 - (var_ponderada/var_geral)
    
    return r2
    
# Verificacao das colunas que tem maior correlacao com o esporte do atleta
for attribute in ['Year', 'Age', 'Height', 'Weight']:
    r_2 = r2(df, 'Sport', attribute)
    print(f'Correlacao entre \'Sport\' e \'{attribute}\'')
    print(f'Coeficiente r_2 = {r_2}\n')