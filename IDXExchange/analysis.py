import pandas as pd

# Read sold CSV
df_sold = pd.read_csv("sold.csv")

print(df_sold.shape)
print(df_sold.columns)
print(df_sold.head())
print(df_sold.describe())
