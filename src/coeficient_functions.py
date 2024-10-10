"""Modulo com funcoes para calculo de coeficiente de associacao entre variaveis"""
import numpy as np
import pandas as pd

from sklearn.feature_selection import SelectKBest, chi2

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
    
    # Calcula as variancias ponderada e geral
    var_ponderada = df_quali_quanti['var'] * df_quali_quanti['qtd']
    var_ponderada = var_ponderada.sum() / df_quali_quanti['qtd'].sum()
    var_geral = df[quanti].std()
    var_geral **= 2
    
    r2 = 1 - (var_ponderada/var_geral)
    
    return r2