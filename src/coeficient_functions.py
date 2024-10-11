"""Modulo com funcoes para calculo de coeficiente de associacao entre variaveis"""
import numpy as np
import pandas as pd

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
    """
    is_sample = int(is_sample)

    # As variaveis quanti e quali devem estar nas colunas do df
    columns = df.columns
    if np.isin(quanti, columns, invert=True) or np.isin(quali, columns, invert=True):
        raise KeyError('Quanti/Quali aren\'t on the columns')

    # A variavel quanti deve ter somente valores numericos
    if any(pd.to_numeric(df[quanti], errors='coerce').isna()):
        raise ValueError('Quanti column has non-numeric values')

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