import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *
from womens_participation import *


df_olymp, df_olymp_countries, df_paralymp, df_paralymp_countries, df2_olymp, df2_olymp_bra, df2_paralymp, df2_paralymp_bra = create_dataframes()

def plot_scatter_graph(df, x, y1, y2, title, score_or_amount):
    # Criando o gráfico de dispersão
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=x, y=y1, data=df, label='Women', color='red', s=70)
    sns.scatterplot(x=x, y=y2, data=df, label='Men', color='blue', s=70)

    # Ajustando o gráfico
    plt.xlabel('Year')
    plt.ylabel(score_or_amount)
    plt.title(title)
    plt.legend(loc='upper left')
    plt.show()
    
    
# Plot dos graficos de dispersao das olimpiadas

df_analysis_aux = df_olymp
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Global)', 'Amount')
df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Global)', 'Score')

df_analysis_aux = df_olymp_countries[df_olymp_countries['NOC']=='BRA']
#lot_scatter_graph(df_analysis_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Brazil)', 'Amount')
df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Brazil)', 'Score')


# Plot dos graficos de dispersao das paralimpiadas

df_analysis_aux = df_paralymp
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Global)', 'Amount')
df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Men\'s Score X Women\'s Score', 'Score')

df_analysis_aux = df_paralymp_countries[df_paralymp_countries['NOC']=='BRA']
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Athletes', 'M_Athletes', 'Scatter Plot: Male Athletes X Female Athletes (Brazil)', 'Amount')
df_analysis_aux = df_analysis_aux[(df_analysis_aux['M_Score'] > 0) | (df_analysis_aux['F_Score'] > 0)]
#plot_scatter_graph(df_analysis_aux, 'Year', 'F_Medal', 'M_Medal', 'Scatter Plot: Men\'s Score X Women\'s Score (Brazil)', 'Score')

def create_table_of_stds():
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
    
    plt.show()