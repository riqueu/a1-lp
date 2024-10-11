import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *
from womens_participation import *


df_olymp, df_olymp_countries, df_paralymp, df_paralymp_countries, df2_olymp, df2_olymp_bra, df2_paralymp, df2_paralymp_bra = create_dataframes()

def plot_scatter_graph(df, x, y1, y2, title, score_or_amount):
    plt.figure()

    # Criando o gráfico de dispersão
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=x, y=y1, data=df, label='Women', color='red', s=70)
    sns.scatterplot(x=x, y=y2, data=df, label='Men', color='blue', s=70)

    # Ajustando o gráfico
    plt.xlabel('Year')
    plt.ylabel(score_or_amount)
    plt.title(title)
    plt.legend(loc='upper left')
    
    return plt
    

# Funcoes auxiliares para o plot dos graficos de dispersao das paralimpiadas e olimpiadas
def filter_paralymp_score_bra():
    df_analysis_aux = df_paralymp_countries[df_paralymp_countries['NOC']=='BRA']
    df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
    return df_analysis_aux

def filter_paralymp_score_global():
    df_analysis_aux = df_paralymp[(df_paralymp['M_Score'] > 0) | (df_paralymp['F_Score'] > 0)]
    return df_analysis_aux
    
def filter_olympic_score_bra():
    df_analysis_aux = df_olymp_countries[df_olymp_countries['NOC']=='BRA']
    df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
    return df_analysis_aux

def filter_olympic_score_global():
    df_analysis_aux = df_olymp[(df_olymp['M_Score'] > 0) | (df_olymp['F_Score'] > 0)]
    return df_analysis_aux

def create_table_of_stds():
    plt.figure()

    df = estimate_statistics(df_olymp_countries[df_olymp_countries['NOC']=='BRA'])
    df = pd.concat([df, estimate_statistics(df_paralymp_countries[df_paralymp_countries['NOC']=='BRA'])])
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