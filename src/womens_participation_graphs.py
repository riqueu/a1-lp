"""Módulo para geração de gráficos de dispersão comparando a participação e desempenho de atletas masculinos e femininos nas Olimpíadas e Paralimpíadas."""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *
from womens_participation import *

olymp_df, olymp_countries_df, paralymp_df, paralymp_countries_df = create_dataframes()

def plot_scatter_graph(df: pd.DataFrame, x: str, y1: str, y2: str, title: str, score_or_amount: str) -> plt:
    """Função que recebe um DataFrame e plota um gráfico de dispersão com os dados de duas variáveis.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem plotados.
        x (str): Nome da coluna do DataFrame a ser usada no eixo x.
        y1 (str): Nome da coluna do DataFrame a ser usada no eixo y para a primeira variável.
        y2 (str): Nome da coluna do DataFrame a ser usada no eixo y para a segunda variável.
        title (str): Título do gráfico.
        score_or_amount (str): Rótulo do eixo y.
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=x, y=y1, data=df, label='Women', color='red', s=70)
    sns.scatterplot(x=x, y=y2, data=df, label='Men', color='blue', s=70)

    plt.xlabel('Year')
    plt.ylabel(score_or_amount)
    plt.title(title, fontsize=20)
    plt.legend(loc='upper left', fontsize='large')
    return plt
    

# Funcoes auxiliares para o plot dos graficos de dispersao das paralimpiadas e olimpiadas
def filter_paralymp_score_bra() -> pd.DataFrame:
    """Prepara o DataFrame para o grafico de dispersão dos atletas brasileiros nas paralimpiadas

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_analysis_aux = paralymp_countries_df[paralymp_countries_df['NOC']=='BRA']
    df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
    return df_analysis_aux

  
def filter_paralymp_score_global() -> pd.DataFrame:
    """Prepara o DataFrame para o grafico de dispersão dos atletas de todos os paises nas paralimpiadas

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_analysis_aux = paralymp_df[(paralymp_df['M_Score'] > 0) | (paralymp_df['F_Score'] > 0)]
    return df_analysis_aux
    
    
def filter_olympic_score_bra() -> pd.DataFrame:
    """Prepara o DataFrame para o grafico de dispersão dos atletas brasileiros nas olimpiadas

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_analysis_aux = olymp_countries_df[olymp_countries_df['NOC']=='BRA']
    df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
    return df_analysis_aux

def filter_olympic_score_global() -> pd.DataFrame:
    """Prepara o DataFrame para o grafico de dispersão dos atletas de todos os paises nas olimpiadas

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_analysis_aux = olymp_df[(olymp_df['M_Score'] > 0) | (olymp_df['F_Score'] > 0)]
    return df_analysis_aux

    
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
    
    # Plot dos graficos de dispersao das olimpíadas
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

  
def create_table_of_stds() -> plt:
    """Plota uma tabela 4x4 com os desvios padrão dos atletas brasileiros nas olimpiadas e paralimpiadas

    Returns:
        plt: Tabela 4x4
    """
    plt.figure()

    df = estimate_statistics(olymp_countries_df[olymp_countries_df['NOC']=='BRA'])
    df = pd.concat([df, estimate_statistics(paralymp_countries_df[paralymp_countries_df['NOC']=='BRA'])])
    df = df.loc['std']
    index = ['Olympic_Std_Normal', 'Olympic_Std_Cleaned', 'Paralympic_Std_Normal', 'Paralympic_Std_Cleaned']
    df = df.set_axis(index).reset_index()
    df.rename(columns={'index': ''}, inplace=True)

    sns.set_theme(style='darkgrid') 
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('tight')   
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    
    return plt