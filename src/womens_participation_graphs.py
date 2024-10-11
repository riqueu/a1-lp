import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from data_cleaner import *
from womens_participation import *


df_olymp, df_olymp_countries, df_paralymp, df_paralymp_countries, df2_olymp, df2_olymp_bra, df2_paralymp, df2_paralymp_bra = create_dataframes()

df_analisys1 = df_olymp
df_analisys1 = df_analisys1[(df_analisys1['M_Score'] > 0) | (df_analisys1['F_Score'] > 0)]

def plot_scatter_graph(df, x, y1, y2):
    # Criando o gráfico de dispersão
    sns.scatterplot(x=x, y=y1, data=df, label=y1, color='purple', s=50, alpha=0.7)
    sns.scatterplot(x=x, y=y2, data=df, label=y2, color='blue', s=50, alpha=0.7)

    # Ajustando o gráfico
    plt.xlabel('Ano')
    plt.ylabel('Quantidade')
    plt.title('Gráfico de Dispersão: Pontuação por Ano')
    plt.legend(title='Grupos')
    plt.show()
    
plot_scatter_graph(df_analisys1, 'Year', 'F_Medal', 'M_Medal')