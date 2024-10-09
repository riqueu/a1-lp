"""Módulo para previsão de dados faltantes em um DataFrame de atletas olímpicos."""

import numpy as np
import pandas as pd
import doctest

from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


def to_encoded(df: pd.DataFrame) -> tuple:
    """ Funcao que recebe um Dataframe e converte as colunas para um formato aceitável para algoritmos do sklearn (somente numeros) e alerta para as colunas 'problematicas', com dados faltando ou mais de um tipo.

    Args:
        df (pd.DataFrame): Dataframe original.

    Returns:
        tuple: Tupla com o Dataframe convertido, uma lista das colunas problematicas, um dicionario com os tipos de cada uma delas, os algoritmos encoders para voltar aos labels originais.
    """
    cols = []
    cols_to_fix = {}
    cols_types = {}
    encoders = {}
    types_colums = df.dtypes.to_dict()
    for column in df.columns:
        # Colunas que tem valores NaN
        if any(df[column].isna()):  
            cols_to_fix[column] = 'Contains NaN'
           
        # Em colunas com tipo object, verifica se ha mais de um
        if types_colums[column] == object:
            df_with_object = df[column].reset_index()
            df_with_object['type'] = df_with_object.apply(lambda x: type(x[column]), axis=1).astype(str)
            types_freq = df_with_object.groupby('type').count()
            types_freq = types_freq[column].index.to_list()
            
            # Tem mais de um tipo
            if len(types_freq) > 1:
                cols_types[column] = types_freq
                cols_to_fix[column] = 'Contains two or more types'
            elif str(types_freq[0]) == str(str):
                cols.append(column)
        
        # Para as colunas numericas, verifica se tem valores negativos
        elif column in cols:
            if any(col < 0 for col in df[column]):
                cols_to_fix[column] = 'Contains Negative'
                cols.remove(column)
                
    # Para as colunas validas, converte os tipos
    for column in cols:
        encoder = LabelEncoder()
        df.loc[:, column] = encoder.fit_transform(df.loc[:, column].astype(str))
        encoders[column] = encoder
        
    return df, cols_to_fix, cols_types, encoders


def fill(means: pd.DataFrame, row: pd.Series) -> pd.Series:
    """ Funcao para preenhcer linhas com mais de uma feature ausente ate deixar somente uma, que sera preenchida com regressao linear

    Args:
        means (pd.DataFrame): Medias das features por 'Sex' e 'Sport'
        row (pd.Series): Linha que esta sendo preenchida

    Returns:
        pd.Series: Linha preenchida, ou com um valor nan para ser removida
    """
    features_nan = row[row.isna()]
    cont_nan = features_nan.shape[0]
    
    # Caso tenha algum um valor NaN, preenche-o com a media ate deixar somente um vazio
    for column in features_nan.index:
        value_column = means.loc[(means['Sex'].astype(str) == row['Sex']) & (means['Sport'].astype(str) == row['Sport']), column]
        if value_column.shape[0] and cont_nan > 1:
            row[column]  = value_column.iloc[0]
            cont_nan -= 1
              
    # Caso nao tenha sido possivel preencher os valores, deixa um nan para que a linha seja removida
    if cont_nan > 1:
        row[-1] = np.nan
        
    return row


def linear_regression(df: pd.DataFrame, features: list, target: str, test_size: float, encoders: list) -> pd.DataFrame:
    """ Funcao que recebe um dataframe e executa sobre ele um algoritmo de regressão linear para preencher as os valores vazios de 'Age', 'Height' e 'Weight'.

    Args:
        df (pd.DataFrame): Dataframe original.
        features (list): Lista com as colunas usadas na regressao linear para prever o valor de target
        target (str): Coluna cujos valores queremos preencher.
        test_size (float): Tamanho do conjunto de dados usados para testar o algoritmo.
        encoders (list): Lista com os algoritmos para converter os valores das colunas para valores bons para o sklearn

    Returns:
        pd.DataFrame: Dataframe com a coluna target preenchida
    """
    # Obtem os conjuntos de treino e de teste
    filter_train = ~df[features].isna()
    filter_train = filter_train.apply(lambda x: sum(x) == 5, axis=1)
    df_train = df.loc[filter_train, features]
        
    y = df_train[target]
    X = df_train[features].drop(target, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    
    # Preenche as linhas com target ausente
    filter_predict = df[target].isna()
    df_to_fill = df.loc[filter_predict, features].drop(target, axis=1)
    df.loc[filter_predict, target] = lin_reg.predict(df_to_fill)
    
    # Varificacao de eficiencia do algoritmo
    y_pred_test = lin_reg.predict(X_test)
    r2 = r2_score(y_test, y_pred_test)
    mean_sq_error = mean_squared_error(y_test, y_pred_test)
    # print(f'Coeficiente r2: {r2}')
    # print(f'Mean sq error: {mean_sq_error}')
    return df


def predict_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Função que preenche valores faltantes de 'Age', 'Height' e 'Weight' com regressão linear
    com base no esporte e sexo do atleta. Se não for possível prever, preenche com a média dos
    valores do esporte e sexo.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'Age', 'Height', 'Weight vazias em algums atletas

    Returns:
        pd.DataFrame: DataFrame com valores faltantes preenchidos.
    """
    df.reset_index(inplace=True)
    features = ['Sex', 'Sport', 'Age', 'Height', 'Weight']
    
    # Preenche linhas que tem 2 ou mais features vazios com a media do esporte e sexo
    filter_nan = df[features].isna()
    filter_nan = filter_nan.apply(lambda x: sum(x) > 1, axis=1)
    means = df[features].groupby(['Sex', 'Sport']).mean().reset_index()
    df.loc[filter_nan, features] = df.loc[filter_nan, features].apply(lambda row: fill(means, row), axis=1)
    
    # Remove as linhas que nao foram preenchidas
    filter_nan = ~df[features].isna()
    filter_nan = filter_nan.apply(lambda x: sum(x) > 3, axis=1)
    df = df.loc[filter_nan]
    
    
    # Converte os valores para um formato bom para o sklearn
    df, columns_to_fix, columns_types, encoders = to_encoded(df)
    
    # print(f'Colunas problematicas: {columns_to_fix}\nTipos das colunas: {columns_types}')
    
    # Para cada coluna target, treinamos um algoritmo e preenchemos os valores vazios
    for target in ['Age', 'Height', 'Weight']:
        df = linear_regression(df, features, target, test_size=0.2, encoders=encoders)
    
    return df
