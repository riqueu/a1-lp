import pandas as pd
from data_cleaner import *

df = pd.read_csv("data/athlete_events.csv")

print("Conferindo se possui todas as colunas necessária")
cleaned_data= dataframe_cleaner(df)
print()
print("dataframe possui todas colunas necessárias")
print()
print("Conferindo os tipos de medahas para int")
cleaned_data = medals_to_int(cleaned_data)
print("Medalhas convertidas")
print()
print("tratando dados faltantes")
cleaned_data = predict_missing(cleaned_data)
print("Dados faltantes tratados")
print()
print("podemos começar")

print(df.head(30))





