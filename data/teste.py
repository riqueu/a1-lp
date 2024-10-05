import pandas as pd


df = pd.read_csv("data/athlete_events.csv")
print(list(df.columns))
print(df.dtypes)