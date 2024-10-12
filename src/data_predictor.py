"""Módulo para previsão de dados faltantes em um DataFrame de atletas olímpicos."""

import numpy as np
import pandas as pd
import doctest

from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder


def to_encoded(df: pd.DataFrame) -> tuple:
    """ Funcao que recebe um Dataframe e converte as colunas para um formato aceitável para algoritmos do sklearn (somente numeros) e alerta para as colunas 'problematicas', com dados faltando ou mais de um tipo.

    Args:
        df (pd.DataFrame): Dataframe original.

    Returns:
        tuple: Tupla com o Dataframe convertido, uma lista das colunas problematicas, um dicionario com os tipos de cada uma delas, os algoritmos encoders para voltar aos labels originais.
    
    Example:
    ----------
    >>> df = pd.DataFrame({
    ...     'Name': ['Alice', 'Bob', 'Charlie', 'Dave'],
    ...     'Age': [25, np.nan, 30, 35],
    ...     'Income': ['High', 'Medium', 'High', 40000],
    ...     'Gender': ['F', 'M', 'M', 'F']
    ... })
    >>> df_encoded, cols_to_fix, cols_types, encoders = to_encoded(df)
    >>> df_encoded
      Name   Age  Income Gender
    0    0  25.0    High      0
    1    1   NaN  Medium      1
    2    2  30.0    High      1
    3    3  35.0   40000      0
    >>> cols_to_fix
    {'Age': 'Contains NaN', 'Income': 'Contains two or more types'}
    >>> cols_types
    {'Income': ["<class 'int'>", "<class 'str'>"]}
    >>> encoders['Name'].inverse_transform([0, 1, 2, 3])
    array(['Alice', 'Bob', 'Charlie', 'Dave'], dtype=object)
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
    
    Example:
    ----------
    >>> means = pd.DataFrame({
    ...     'Height': {('M', 'Soccer'): 180, ('M', 'Basketball'): 200},
    ...     'Weight': {('M', 'Soccer'): 75, ('M', 'Basketball'): 90}
    ... })
    
    >>> row = pd.Series({'Sex': 'M', 'Sport': 'Basketball', 'Height': np.nan, 'Weight': 88})
    >>> fill(means, row)
    Sex                M
    Sport     Basketball
    Height           NaN
    Weight            88
    dtype: object
    """
    features_nan = row[row.isna()]
    cont_nan = features_nan.shape[0]
    
    # Caso tenha algum um valor NaN, preenche-o com a media ate deixar somente um vazio
    for column in features_nan.index:
        key = (row['Sex'], row['Sport'])
        try:
            value_column = means[key][column]
            if cont_nan <= 1:
                break
            elif value_column:
                row[column] = value_column
                cont_nan -= 1
        except KeyError:
            # Caso a chave (Sex, Sport) não exista no dicionário means
            continue
        except Exception as e:
            # Para qualquer outro tipo de erro
            print(f"Erro ao preencher a coluna {column}: {e}")
            continue
        
    return row


def linear_regression(df: pd.DataFrame, features: list, target: str, test_size: float) -> pd.DataFrame:
    """ Funcao que recebe um dataframe e executa sobre ele um algoritmo de regressão linear para preencher as os valores vazios de 'Age', 'Height' e 'Weight'.
    Args:
        df (pd.DataFrame): Dataframe original.
        features (list): Lista com as colunas usadas na regressao linear para prever o valor de target
        target (str): Coluna cujos valores queremos preencher.
        test_size (float): Tamanho do conjunto de dados usados para testar o algoritmo.
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
    root_mean_sq_error = root_mean_squared_error(y_test, y_pred_test)
    # print(f'Coeficiente r2: {r2}')
    # print(f'Root mean ean sq error: {root_mean_sq_error}')
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
    features = ['Sex', 'Sport', 'Age', 'Height', 'Weight']

    # Preenche linhas que tem 2 ou mais features vazios com a media do esporte e sexo
    filter_nan = df[features].isna()
    filter_nan = filter_nan.apply(lambda x: sum(x) > 1, axis=1)
    means = df[features].groupby(['Sex', 'Sport']).mean().to_dict(orient='index')
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
        df = linear_regression(df, features, target, test_size=0.2)
    
    # Retorna os valores encodificados de volta aos originais
    for column in encoders.keys():
        df.loc[:, column] = encoders[column].inverse_transform(df[column].astype(int))

    return df

if __name__ == "__main__":
     doctest.testmod(verbose=False)

# data = {
#     'Age': [25, np.nan, 30, 35, np.nan, 45, np.nan, 40, 29, 31, np.nan, 34, 36, np.nan, 27],
#     'Height': [175, 180, np.nan, 165, 170, 160, np.nan, 168, 176, 158, 177, 180, np.nan, 169, 171],
#          'Weight': [70, 75, 80, np.nan, 65, 85, 90, 88, 72, np.nan, 78, 77, 74, np.nan, 68],
#          'Sex': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#          'Sport': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
#  }
# df = pd.DataFrame(data)
# features = ['Age', 'Height', 'Weight', 'Sex', 'Sport']
# filled_df = linear_regression(df, features, 'Age', 0.2)
# print(filled_df['Age'].isna().sum())