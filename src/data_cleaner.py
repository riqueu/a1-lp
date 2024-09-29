"""Módulo com funções para limpeza de dados."""

import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def medals_to_int(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe DataFrame com coluna 'Medal' e converte valores string para inteiros.
    0: Sem medalha; 1: Bronze; 2: Prata; 3: Ouro.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Medal'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Medal' convertida para inteiros.
    """
    df['Medal'] = df['Medal'].map({'Gold': 3, 'Silver': 2, 'Bronze': 1})
    df['Medal'] = df['Medal'].fillna(0)
    df['Medal'] = df['Medal'].astype(int)
    
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
    for sport in df['Sport'].unique():
        for sex in df['Sex'].unique():
            # Filtra o dataframe para pegar apenas o esporte e sexo em questão
            subset = df[(df['Sport'] == sport) & (df['Sex'] == sex)]
            target_columns = ['Age', 'Height', 'Weight']
            
            # Preenche cada com regressão linear
            for target in target_columns:
                # Cria um subconjunto de linhas onde a coluna alvo não está faltando
                available_data = subset.dropna(subset=[target])
                predictors = [col for col in target_columns if col != target]
                
                # Se faltam todos, cai no caso que não usa regressão linear e preenche com a média do esporte e sexo
                if available_data[predictors].isnull().all().any():
                    continue
                
                # Extrai os dados de treino e teste
                X_train, _, y_train, _ = train_test_split(available_data[predictors], available_data[target], test_size=0.2, random_state=0)
                
                # Use uma pipeline para preencher os valores faltantes
                imputer = SimpleImputer(strategy='mean')  # estratégia de média
                reg = LinearRegression()
                pipeline = make_pipeline(imputer, reg)
                
                # Ajusta o modelo usando o pipeline
                pipeline.fit(X_train, y_train)
            
                # Acha as linhas onde a coluna alvo está faltando
                missing_data = subset[subset[target].isnull()]
                
                if not missing_data.empty:
                    # Usa modelo para prever valores faltantes
                    X_missing = missing_data[predictors]
                    
                    # Só prever se os preditores tiverem valores não faltantes
                    if not X_missing.isnull().all(axis=1).any():
                        predicted_values = pipeline.predict(X_missing)
                        df.loc[(df['Sport'] == sport) & (df['Sex'] == sex) & (df[target].isnull()), target] = predicted_values
                    
            # Preenche os valores faltantes com a média dos valores daquele esporte e sexo
            df[target_columns] = df.groupby(['Sex', 'Sport'])[target_columns].transform(lambda x: x.fillna(x.mean())).round(1)
    
    df.dropna(inplace=True) # Remove NaN's que não foram preenchidos (~ que faltaram informações para preencher)
    
    # Arredonda os valores das target_columns e tranforma em inteiro 
    for col in target_columns:
        df[col] = df[col].round(0).astype(int)

    return df
