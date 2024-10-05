"""Módulo com funções para limpeza de dados."""

import numpy as np
import pandas as pd
import doctest

from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def dataframe_cleaner(dataframe: pd.DataFrame) -> pd.DataFrame:
    """A função que confere se  possui todas as colunas necessárias para análise

    Args:
        df (pd.DataFrame): dataframe
        
        Index:
            RangeIndex
        Columns:
            Name: 'ID' - Unique number for each athlete
            Name: 'Name' - Athlete's name
            Name: 'Sex' - M or F
            Name: 'Age' - Integer
            Name: 'Height' - In centimeters
            Name: 'Weight' - In kilograms
            Name: 'Team' - Team name
            Name: 'NOC' - National Olympic Committee 3-letter code
            Name: 'Games' - Year and season
            Name: 'Year' - Integer
            Name: 'Season' - Summer or Winter
            Name: 'City' - Host city
            Name: 'Sport' - Sport
            Name: 'Event' - Event
            Name: 'Medal' - Gold, Silver, Bronze, or NA
        
    Returns:
        pd.DataFrame: a cleaned dataframe
    """
    
    # creates a copy of the original dataset
    df = dataframe.copy()
    
    useful_columns = ['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    
    try:
        useful_df = df[useful_columns]
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it.")
        quit()
    else:
        return useful_df
    
def medals_to_int(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe DataFrame com coluna 'Medal' e converte valores string para inteiros.
    0: Sem medalha; 1: Bronze; 2: Prata; 3: Ouro.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'Medal'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'Medal' convertida para inteiros.
    
    Example
    ----------
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': ['Gold', 'Gold', 'Silver', 'Bronze', np.nan]  })
    >>> cleaned_data = medals_to_int(data)
    >>> print(cleaned_data['Medal'].tolist())
    [3, 3, 2, 1, 0]
    
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': [np.nan, 'Bronze', 'Bronze', 'Bronze', np.nan]  }) 
    >>> cleaned_data =  medals_to_int(data)
    >>> print(cleaned_data['Medal'].tolist())
    [0, 1, 1, 1, 0]
    
    >>> data = pd.DataFrame({'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 'Medal': [np.nan, np.nan, np.nan, np.nan, np.nan]  }) 
    >>> cleaned_data =  medals_to_int(data)
    >>> print(cleaned_data['Medal'].tolist())
    [0, 0, 0, 0, 0]
    """
    try:
        df['Medal'] = df['Medal'].map({'Gold': 3, 'Silver': 2, 'Bronze': 1})
        df['Medal'] = df['Medal'].fillna(0)
        df['Medal'] = df['Medal'].astype(int)
        
    except KeyError:
        print(
            f"The given dataframe has no column 'Medal', consider replacing it.")
        quit()
    else:
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
    
    # TODO
    #  Analisar os casos onde há apenas uma linha com aquele parametro (sexo, esporte, peso, idade, altura)
    #  Por exemplo: Se num dataframe  de um determinado país num esporte há apenas um atleta que não possui a altura informada
    #  O programa executaria erro, pois não teria como comparar com outros atletas
    
    try:
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
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it.")
        quit()
    else:
        return df


if __name__ == "__main__":
     doctest.testmod(verbose=True)