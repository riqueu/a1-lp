import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *
from womens_participation import *

def plot_scatter_graph(df: pd.DataFrame, x: str, y1: str, y2: str, title: str, score_or_amount: str) -> plt:
    """Função que recebe um DataFrame e plota um gráfico de dispersão com os dados de duas variáveis.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem plotados.
        x (str): Nome da coluna do DataFrame a ser usada no eixo x.
        y1 (str): Nome da coluna do DataFrame a ser usada no eixo y para a primeira variável.
        y2 (str): Nome da coluna do DataFrame a ser usada no eixo y para a segunda variável.
        title (str): Título do gráfico.
        score_or_amount (str): Rótulo do eixo y.

    Returns:
        plt: Objeto matplotlib.pyplot com o gráfico de dispersão.
    """
    # Criando o gráfico de dispersão
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=x, y=y1, data=df, label='Women', color='purple', s=70)
    sns.scatterplot(x=x, y=y2, data=df, label='Men', color='blue', s=70)

    # Ajustando o gráfico
    plt.xlabel('Year')
    plt.ylabel(score_or_amount)
    plt.title(title)
    plt.legend(loc='upper left', fontsize='large')
    return plt
    
def create_all_graphs(athletes_df: pd.DataFrame, modified_medal_athlete_df: pd.DataFrame, summer_paralympics_df: pd.DataFrame, winter_paralympics_df: pd.DataFrame) -> list:
    """
    Generates a series of scatter plots comparing male and female athletes' participation and performance in both the Olympics and Paralympics.
    Args:
        athletes_df (pd.DataFrame): DataFrame containing data on Olympic athletes.
        modified_medal_athlete_df (pd.DataFrame): DataFrame containing modified data on medal-winning athletes.
        summer_paralympics_df (pd.DataFrame): DataFrame containing data on Summer Paralympic athletes.
        winter_paralympics_df (pd.DataFrame): DataFrame containing data on Winter Paralympic athletes.
    
    Returns:
        list: A list of scatter plot objects.
    """
    df_olymp, df_olymp_countries, df_paralymp, df_paralymp_countries, _, _, _, _ = create_dataframes(athletes_df, modified_medal_athlete_df, summer_paralympics_df, winter_paralympics_df)
    
    plots = []
    
    df_analisys_aux = df_olymp
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Global)', 'Amount'))
    df_analisys_aux = df_analisys_aux[(df_analisys_aux['M_Score'] > 0) | (df_analisys_aux['F_Score'] > 0)]
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Global)', 'Score'))

    df_analisys_aux = df_olymp_countries[df_olymp_countries['NOC']=='BRA']
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Brazil)', 'Amount'))
    df_analisys_aux = df_analisys_aux[(df_analisys_aux['M_Score'] > 0) | (df_analisys_aux['F_Score'] > 0)]
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Brazil)', 'Score'))


    # Plot dos graficos de dispersao das paralimpiadas

    df_analisys_aux = df_paralymp
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Global)', 'Amount'))
    df_analisys_aux = df_analisys_aux[(df_analisys_aux['M_Score'] > 0) | (df_analisys_aux['F_Score'] > 0)]
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Men\'s Score X Women\'s Score', 'Score'))

    df_analisys_aux = df_paralymp_countries[df_paralymp_countries['NOC']=='BRA']
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Brazil)', 'Amount'))
    df_analisys_aux = df_analisys_aux[(df_analisys_aux['M_Score'] > 0) | (df_analisys_aux['F_Score'] > 0)]
    plots.append(plot_scatter_graph(df_analisys_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Brazil)', 'Score'))
    
    return plots
