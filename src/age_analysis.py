import pandas as pd
from data_cleaner import *
import matplotlib.pyplot as plt
import seaborn as sns 


def estatisticas_idade_por_esporte(df: pd.DataFrame) -> dict:
    """
    Função que agrupa o DataFrame pela coluna 'Sport' e calcula mediana, 1º quartil (Q1) e 3º quartil (Q3)
    apenas para a coluna 'Age'.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos.
    
    Returns:
        dict: Um dicionário contendo as estatísticas da coluna 'Age' para cada esporte.
    """
    
    # Verifica se as colunas 'Sport' e 'Age' existem no DataFrame
    if 'Sport' not in df.columns or 'Age' not in df.columns:
        raise ValueError("As colunas 'Sport' e/ou 'Age' não estão presentes no DataFrame.")
    
    # Inicializando um dicionário para armazenar os resultados
    estatisticas = {}
    
    # Agrupando o DataFrame pela coluna 'Sport'
    grouped = df.groupby('Sport')

    # Iterando por cada grupo (esporte)
    for sport, group in grouped:
        estatisticas[sport] = {}
        
        # Selecionando a coluna 'Age'
        idade = group['Age']

        # Dados estatísticos da coluna 'Age' para aquele esporte 
        estatisticas[sport]['mediana'] = idade.median()
        estatisticas[sport]['1º quartil'] = idade.quantile(0.25)
        estatisticas[sport]['3º quartil'] = idade.quantile(0.75)
        estatisticas[sport]['minimo'] = idade.min()
        estatisticas[sport]['maximo'] = idade.max()
        estatisticas[sport]['media'] = idade.mean()
        estatisticas[sport]['desvio_padrao'] = idade.std()
        estatisticas[sport]['variancia'] = idade.var()
        
        #  Calculando os limites inferiores e superiores com base da idade
        interquartil = idade.quantile(0.75) - idade.quantile(0.25)
        limite_inferior = idade.quantile(0.25) - interquartil*1.5
        limite_superior = idade.quantile(0.75) + interquartil*1.5
        
        # Por serem variáveis discretas
        estatisticas[sport]['limite inferior'] = round(limite_inferior)
        estatisticas[sport]['limite superior'] = round(limite_superior) 
        
    
    return estatisticas


def esportes_com_idades_extremas(df: pd.DataFrame) -> list:
    """
    Função que verifica quais esportes têm atletas com idades menores que o 1º quartil
    ou maiores que o 3º quartil e retorna uma lista desses esportes.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos.
    
    Returns:
        list: Lista de esportes que possuem atletas com idades extremas.
    """
    
    # Verifica se as colunas 'Sport' e 'Age' existem no DataFrame
    if 'Sport' not in df.columns or 'Age' not in df.columns:
        raise ValueError("As colunas 'Sport' e/ou 'Age' não estão presentes no DataFrame.")
    
    # Inicializando a lista para armazenar esportes com idades extremas
    esportes_extremos = {}
    
    # Agrupando o DataFrame pela coluna 'Sport'
    grouped = df.groupby('Sport')
    
    # Iterando por cada grupo (esporte)
    for sport, group in grouped:
        # Selecionando a coluna 'Age'
        idade = group['Age']
        
        # Calculando 1º quartil (Q1) e 3º quartil (Q3)
        q1 = idade.quantile(0.25)
        q3 = idade.quantile(0.75)
        interquartil = q3 - q1
        limite_inferior= q1 -1.5*interquartil
        limite_superior = q3+ 1.5*interquartil
        
        # Verificando se há idades fora do intervalo (menor que Q1 ou maior que Q3)
  
        contagem_extremos = ((idade < limite_inferior) | (idade > limite_superior)).sum()

        
        if contagem_extremos > 0:
            esportes_extremos[sport] = contagem_extremos
            
    return esportes_extremos


# Esportes Com Outliers
def esportes_outliers_save_graph(df: pd.DataFrame) -> None:
    """
    Função que gera um boxplot com os esportes que possuem atletas com idades extremas.
    
    Args:
        cleaned_data (pd.DataFrame): O DataFrame com os dados esportivos limpos.
    """
    esportes_extremos = esportes_com_idades_extremas(df)
    # Analisando o esporte com mais valores extremos
    maior_esporte = max(esportes_extremos, key=esportes_extremos.get)
    quantidade = esportes_extremos[maior_esporte]

    df_maioresporte = df[df['Sport'] == maior_esporte]

    sns.boxplot(x='Sport', y='Age', data=df_maioresporte)
    plt.title('Boxplot de Idades por Esporte')
    plt.xlabel('Esporte')
    plt.ylabel('Idade')

    # Salvando o gráfico como PNG
    plt.savefig('graphs/bloxplot_gymnastics_age.png', format='png', dpi=300)
