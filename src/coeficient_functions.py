"""Modulo com funcoes para calculo de coeficiente de associacao entre variaveis"""
import numpy as np
import pandas as pd
import doctest
import math
from sklearn.feature_selection import SelectKBest, chi2


def r2(df: pd.DataFrame, quali: str, quanti: str, is_sample: bool = True) -> float:
    """ Funcao que calcula o coeficiente R2, que quantifica a correlacao entre uma variavel qualitativa e um quantitativa

    Args:
        df (pd.DataFrame): Dataframe com todos os dados
        quali (str): Coluna com os valores da variavel qualitativa
        quanti (str): Coluna com os valores da variavel quantitativa
        is_sample (bool, optional): Informacao se os dados sao de uma amostra ou nao (de uma populacao). Defaults to True.

    Returns:
        float: Coeficiente R2
    
    Example:
    ----------
    >>> df = pd.DataFrame({
    ...     'qualitativa': ['A', 'A', 'B', 'B', 'C', 'C'],
    ...     'quantitativa': [1, 2, 3, 4, 5, 6]
    ... })
    >>> r2(df, 'qualitativa', 'quantitativa')
    0.8571428571428571
    """
    is_sample = int(is_sample)

    # As variaveis quanti e quali devem estar nas colunas do df
    columns = df.columns
    if np.isin(quanti, columns, invert=True) or np.isin(quali, columns, invert=True):
        raise KeyError('Quanti/Quali aren\'t on the columns')
        quit()
    # A variavel quanti deve ter somente valores numericos
    if any(pd.to_numeric(df[quanti], errors='coerce').isna()):
        raise ValueError('Quanti column has non-numeric values')
        quit()
    # Agrupa o dataframe pela coluna quali e calcula as medidas resumos para a variavel quanti em cada categoria quali
    df_quali_quanti = df[[quali, quanti]].groupby(quali).agg(
        qtd=(quanti, 'count'),
        mean=(quanti, 'mean'),
        var=(quanti, lambda x: x.std(ddof=is_sample)),
        max=(quanti, 'max'),
        min = (quanti, 'min')
    )
    df_quali_quanti['var'] = df_quali_quanti['var'] ** 2

    # Calcula as variancias ponderada e geral
    var_ponderada = df_quali_quanti['var'] * df_quali_quanti['qtd']
    var_ponderada = var_ponderada.sum() / df_quali_quanti['qtd'].sum()
    var_geral = df[quanti].std(ddof=is_sample)
    var_geral **= 2

    r2 = 1 - (var_ponderada/var_geral)

    return r2


def corr(df: pd.DataFrame, quanti_1: str, quanti_2: str, is_sample: bool = True) -> float:
    """ Funcao que calcula o coeficiente de correlacao, que quantifica a associacao entre duas variaveis quantitativas

    Args:
        df (pd.DataFrame): Dataframe com todos os dados
        quanti_1 (str): Coluna com os valores da primeira variavel quantitativa
        quanti_2 (str): Coluna com os valores da segunda variavel quantitativa
        is_sample (bool, optional): Informacao se os dados sao de uma amostra ou nao (de uma populacao). Defaults to True.

    Returns:
        float: Coeficiente de correlacao
    
    Example:
    ----------
    >>> df = pd.DataFrame({
    ...     'x': [1, 2, 3, 4, 5],
    ...     'y': [2, 4, 6, 8, 10]
    ... })
    >>> corr(df, 'x', 'y')
    0.9999999999999998

    >>> df2 = pd.DataFrame({
    ...     'a': [1, 2, 3, 4, 5],
    ...     'b': [5, 4, 3, 2, 1]
    ... })
    >>> corr(df2, 'a', 'b')
    -0.9999999999999998
    """
    is_sample = int(is_sample)
    # Calcula a covariancia das variaveis e os desvios padrao
    quanti_1_center = df[quanti_1] - df[quanti_1].mean()
    quanti_2_center = df[quanti_2] - df[quanti_2].mean()

    std_1 = df[quanti_1].std(ddof = is_sample)
    std_2 = df[quanti_2].std(ddof = is_sample)

    cov = quanti_1_center * quanti_2_center
    cov = cov.sum() / (df.shape[0] - is_sample)

    corr = cov / (std_1 * std_2)

    return corr

def qui2(df, quali1, quali2, is_sample=True):
    # Agruprando pelas classes iguais
    df = df.groupby([quali1, quali2]).count()
    # display(df.head())
    df = df.unstack(level=quali2)
    df['Total'] = df.apply('sum', axis=1)
    df.loc['Total', :] = df.apply('sum')

    # Calcula as frequencias relativas as colunas
    df_relative = df.apply(lambda x: x/x[:-1].sum())
    df_expected = df.apply(lambda x: x*df_relative.Total)

    df_qui = (df - df_expected)**2
    df_qui /= df_expected
    
    # display(df)
    
    # display(df_relative)

    # display(df_expected)

    # display(df_qui)

    qui2 = df_qui.iloc[:-1, :-1].sum().sum()

    return qui2, df.shape[0]-1, df.shape[1]-1
    

def coeficientes_qui2(df: pd.DataFrame, quali_1: str, quali_2: str, is_sample: bool =True) -> float:
    
    # Obtem o qui2
    qui_2, rows, columns = qui2(df, quali_1, quali_2, is_sample)
    
    # Coeficiente de contigencia
    C = math.sqrt(qui_2/(qui_2+df.shape[0]))

    # Coeficente T
    T = math.sqrt(qui_2/(df.shape[0].math.sqrt((rows-1)(columns-1))))

    # Coeficient V Cramer
    V = math.sqrt(qui_2/(df.shape[0]*min([rows, columns])))
     
    return C, T, V


if __name__ == "__main__":
     doctest.testmod(verbose=False)
