import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('January 2024 to Current Day.csv')
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(r'\n','',regex=True)
df.columns = df.columns.str.replace(r'\r','',regex=True)
df.columns = df.columns.str.replace(r'\t','',regex=True)
df.columns = df.columns.str.replace(' ','_',regex=True)

df[['Chemical','Bath']] = df['Phase'].str.split(' ', n=1, expand=True)


# df.to_csv('atp.csv')





#
print(
    df['Chemical'].unique()
      )
# c = df.groupby('Chemical')['Chemical'].nunique()
# print ( 
#     c
    
#     )
# print (pd.DataFrame.from_records(c.values.tolist()).stack().value_counts())