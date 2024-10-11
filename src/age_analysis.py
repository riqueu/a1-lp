"""Modulo com as funções da hipotese de Idades"""
import pandas as pd
from data_cleaner import *
import matplotlib.pyplot as plt
import seaborn as sns 
import doctest


def statistics_by_age(df: pd.DataFrame) -> dict:
    """Função que agrupa o DataFrame pela coluna 'Sport' e calcula mediana, 1º quartil (Q1) e 3º quartil (Q3)
    apenas para a coluna 'Age'.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos.
    
    Returns:
        dict: Um dicionário contendo as estatísticas da coluna 'Age' para cada esporte.
    
    Example
    ----------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'Sport': ['Soccer', 'Basketball', 'Tennis', 'Soccer', 'Basketball', 'Tennis'],
    ...     'Age': [20, 35, 25, 21, 45, 19]
    ... })
    >>> statistics_by_age(df)
    {'Basketball': {'mediana': 40.0, '1º quartil': 37.5, '3º quartil': 42.5, 'minimo': 35, 'maximo': 45, 'media': 40.0, 'desvio_padrao': 7.0710678118654755, 'variancia': 50.0, 'limite inferior': 30, 'limite superior': 50}, 'Soccer': {'mediana': 20.5, '1º quartil': 20.25, '3º quartil': 20.75, 'minimo': 20, 'maximo': 21, 'media': 20.5, 'desvio_padrao': 0.7071067811865476, 'variancia': 0.5, 'limite inferior': 20, 'limite superior': 22}, 'Tennis': {'mediana': 22.0, '1º quartil': 20.5, '3º quartil': 23.5, 'minimo': 19, 'maximo': 25, 'media': 22.0, 'desvio_padrao': 4.242640687119285, 'variancia': 18.0, 'limite inferior': 16, 'limite superior': 28}}
    """
    # Inicializando um dicionário para armazenar os resultados
    estatisticas = {}
    
    try:
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
            
    except KeyError:
            print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
            quit()
    else:
        return estatisticas


def highest_age_aplitude_sports(df: pd.DataFrame) -> dict:
    """
    Função que verifica quais esportes têm atletas com idades menores que o 1º quartil
    ou maiores que o 3º quartil e retorna uma lista desses esportes.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos.
    
    Returns:
        dict: dicionario com os  esportes que possuem atletas com idades extremas.
    
    Example
    ----------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'Sport': ['Soccer']*10 + ['Basketball']*10 + ['Tennis']*10 + ['Swimming']*10 + 
    ...              ['Boxing']*10 + ['Volleyball']*10 + ['Golf']*10,
    ...     'Age': [20, 22, 45, 23, 21, 60, 18, 27, 29, 24, # Soccer
    ...             30, 32, 35, 45, 38, 55, 19, 25, 50, 21, # Basketball
    ...             19, 20, 40, 60, 23, 25, 55, 28, 30, 26, # Tennis
    ...             15, 28, 34, 35, 33, 18, 24, 22, 25, 45, # Swimming
    ...             17, 55, 29, 30, 32, 36, 20, 31, 33, 27, # Boxing
    ...             23, 45, 25, 28, 26, 44, 29, 27, 48, 22, # Volleyball
    ...             65, 70, 58, 55, 62, 64, 66, 67, 60, 59] # Golf
    ... })
    >>> highest_age_aplitude_sports(df)
    {'Boxing': 2, 'Soccer': 2, 'Tennis': 1}
    """
    # Inicializando o dicionario para armazenar esportes com idades extremas
    esportes_extremos = {}
    
    # Agrupando o DataFrame pela coluna 'Sport'
    try:
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
    
    except KeyError:
            print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
            quit()
    else:
        return esportes_extremos


def create_boxplot_sport_with_the_most_outliers(df: pd.DataFrame) -> plt:
    """Função que gera um boxplot com o esporte que possui mais atletas com idades extremas.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos limpos.
        
    Returns:
        plt: Um objeto do tipo matplotlib.pyplot com o boxplot
    
    Example
    ----------
    >>> import pandas as pd
    >>> import numpy as np 
    >>> data = pd.DataFrame({
    ...    'Atleta': ['Jaime', 'Walleria', 'Carlos', 'Henrique', 'Novaes'], 
    ...    'Medal': ['Gold', 'Gold', 'Silver', 'Bronze', np.nan], 
    ...    'Age': [80, 20, 19, 19, 18], 
    ...    'Sport': ['Volleybol', 'Volleybol', 'Volleybol', 'Volleybol', 'Volleybol']})       
    >>> plot = create_boxplot_sport_with_the_most_outliers(data)
    >>> plot.__class__.__name__ == "module"
    True

    """
    try:
        esportes_extremos = highest_age_aplitude_sports(df)
        # Analisando o esporte com mais valores extremos
        maior_esporte = max(esportes_extremos, key=esportes_extremos.get)
        quantidade = esportes_extremos[maior_esporte]
        
        df_maioresporte = df[df['Sport'] == maior_esporte]

        plt.figure()
        boxplot = sns.boxplot(x='Sport', y='Age', data=df_maioresporte)
        boxplot.set_yscale('linear')
        plt.title('Age Boxplot by Sport')
        plt.xlabel('Sport')
        plt.ylabel('Age')

        return plt
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
        quit()
    except ValueError:
        print(f"The given dataframe does not have sports with outliers")
        quit()


def create_boxplot_top_3_esportes_outliers(df: pd.DataFrame)-> plt:
    """Função que gera um boxplot com as idades dos  3 esportes que possuem mais atletas com idades extremas.

    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos limpos.
        
    Returns:
        plt: Um objeto do tipo matplotlib.pyplot com o boxplot
    
    Example
    ----------
    >>> import pandas as pd
    >>> import numpy as np
    >>> data = pd.DataFrame({
    ...     'Sport': ['Soccer', 'Basketball', 'Tennis', 'Swimming', 'Soccer', 'Basketball', 
    ...               'Tennis', 'Swimming', 'Soccer', 'Basketball', 'Tennis', 'Swimming',
    ...               'Soccer', 'Basketball', 'Tennis', 'Swimming', 'Boxing', 'Boxing',
    ...               'Boxing', 'Boxing'],
    ...     'Age': [20, 35, 25, 23, 45, 15, 22, 28, 60, 14, 32, 20, 17, 50, 21, 26, 
    ...             19, 30, 55, 41]
    ... })
    >>> plot = create_boxplot_top_3_esportes_outliers(data)
    >>> plot.__class__.__name__ == "module"
    True
    """
    try:
        esportes_extremos = highest_age_aplitude_sports(df)
        #  Top 3 esportes com mais outliers de idade
        top_3_extremos =  sorted(esportes_extremos.items(), key=lambda item: item[1], reverse=True)[:3]
        nomes_top_3 = [esporte for esporte, _ in top_3_extremos]    

        df_top_3_extremos =  df[df['Sport'].isin(nomes_top_3)]
        
        # Criando o boxplot com os 3 esportes com mais outliers
        plt.figure()
        boxplots = sns.boxplot(x='Sport', y='Age', data=df_top_3_extremos)
        boxplots.set_yscale('linear')


        # Adicionando título e rótulos
        plt.title('Age Boxplot by Sport')
        plt.xlabel('Sport')
        plt.ylabel('Age')
        
        return plt
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
        quit()
    except ValueError:
        print(f"The given dataframe does not have sports with outliers")
        quit()


def create_boxplot_top_3_esportes_most_awarded(df: pd.DataFrame) -> plt:
    """Função que gera um boxplot  de idade com os  3 esportes
    mais premiados pro brasileiros.
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos limpos.

    Returns:
        plt: Um objeto do tipo matplotlib.pyplot com o boxplot
    
    Example
    ----------
    >>> import pandas as pd
    >>> df_example = pd.DataFrame({
    ...     'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA', 'BRA', 'BRA', 'BRA'],
    ...     'Sport': ['Soccer', 'Volleyball', 'Swimming', 'Swimming', 'Soccer', 'Soccer', 'Judo', 'Volleyball', 'Judo', 'Judo'],
    ...     'Medal': [1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    ...     'Age': [22, 24, 20, 23, 27, 26, 28, 25, 22, 24]
    ... })
    >>> plot = create_boxplot_top_3_esportes_most_awarded(df_example)
    >>> plot.__class__.__name__ == "module"
    True
    """
    try:
        #  Filtrando os atletas brasileiros
        atletas_brasileiros =  df[df['NOC'] == 'BRA']
        
        medalhas_br_por_esporte = atletas_brasileiros.groupby('Sport')['Medal'].sum()
        top_3_esportes = medalhas_br_por_esporte.sort_values(ascending=False).head(3)
        nome_dos_3_esportes_mais_premiados = top_3_esportes.index.tolist()
        
        df_top_3_mais =  atletas_brasileiros[atletas_brasileiros['Sport'].isin(nome_dos_3_esportes_mais_premiados)]
        
        # Criando o boxplot com os 3 esportes com mais outliers
        plt.figure()
        sns.boxplot(x='Sport', y='Age', data=df_top_3_mais)

        # Adicionando título e rótulos
        plt.title('Boxplot of Ages of the Most Awarded Sports by Brazil')
        plt.xlabel('Sport')
        plt.ylabel('Age')

        return plt
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
        quit()
        

def create_boxplot_age_medal_status_brazil(df: pd.DataFrame) -> plt:
    """Cria um boxplot de idade com as categorias atletas brasileiros premiados 
    e atletas brasileiros não premiados
    
    Args:
        df (pd.DataFrame): O DataFrame com os dados esportivos limpos.

    Returns:
        plt: Um objeto do tipo matplotlib.pyplot com o boxplot
    
    Example
    ----------
    >>> import pandas as pd
    >>> df_example = pd.DataFrame({
    ...     'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA', 'BRA'],
    ...     'Medal': [1, 0, 1, 0, 1, 0, 1, 0],
    ...     'Age': [22, 24, 20, 23, 27, 26, 28, 25]
    ... })
    >>> plot = create_boxplot_age_medal_status_brazil(df_example)
    >>> plot.__class__.__name__ == "module"
    True
        
    Returns:
        plt: Um objeto do tipo matplotlib.pyplot com o boxplot
    """
    try:   
    #  Criando coluna que informa se o atleta foi premiado ou não
        df.loc[:, 'Medal'] = df['Medal'].apply(lambda x: 1 if x in [1, 2, 3] else 0)

        #  Filtrando os atletas brasileiros
        atletas_brasileiros =  df[df['NOC'] == 'BRA']
        
        # Criando os boxplots com as idades dos medalhistas e não medalhistas
        plt.figure()
        sns.boxplot(x='Medal', y='Age', data=atletas_brasileiros)

        # Adicionando título e rótulos
        plt.title('Boxplot of Ages of Awarded and Non-Awarded Brazilian Athletes')
        plt.xlabel('Was Awarded')
        plt.xticks([0, 1], ['Not Awarded', 'Awarded'])
        plt.ylabel('Age')

        # Exibindo o gráfico
        return plt
        
    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
        quit()    
    

def create_boxplot_age_by_medals_athletes_in_brazil(df: pd.DataFrame) -> plt:
    """Cria um boxplot com as idades dos atletas premiados pelo brasil e 
    categoriza por tipo de medalha 

    Args:
        df (pd.DataFrame): dataframe limpo

    Returns:
        plt:  Um objeto do tipo matplotlib.pyplot com o boxplot
    
    Example
    ----------
     >>> import pandas as pd
    >>> df_example = pd.DataFrame({
    ...     'NOC': ['BRA', 'BRA', 'BRA', 'BRA', 'USA', 'BRA', 'BRA'],
    ...     'Medal': ['3', '2', '1', 0, '3', '3', '2'],
    ...     'Age': [22, 24, 20, 23, 27, 26, 28]
    ... })
    >>> plot = create_boxplot_age_by_medals_athletes_in_brazil(df_example)
    >>> plot.__class__.__name__ == "module"
    True
    """
    
    try:
        #  Filtrando os atletas brasileiros
        atletas_brasileiros =  df[df['NOC'] == 'BRA']
        plt.figure()
        sns.boxplot(x='Medal', y='Age', data=atletas_brasileiros)

        # Adicionando título e rótulos
        plt.title('Age Boxplot of Brazilian Athletes by Medals')
        plt.xlabel('Medal')
        plt.ylabel('Age')

        return plt
    

    except KeyError:
        print(
            f"The given dataframe doesn't have all needeed columns, consider replacing it")
            
        quit()


if __name__ == "__main__":
     doctest.testmod(verbose=False)
