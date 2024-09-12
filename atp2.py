import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate sample time-series data
np.random.seed(42)
dates = [datetime.now() - timedelta(days=i) for i in range(100)]
y1 = np.random.rand(100) * 10
y2 = np.random.rand(100) * 20
y3 = np.random.rand(100) * 30
y4 = np.random.rand(100) * 40

#
df = pd.read_csv('atp.csv'); df['Start_Time'] = pd.to_datetime(df['Start_Time'],format='%m/%d/%Y %H:%M:%S %p'); 
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'])
# df = df[df['Start_Time'] > '1/1/2024']
df = df[df['TargetVol_(mL)'] > 3000]

#
figs = []
for c in (df['Chemical'].unique()):
    # print (c)
    df2=df[df['Chemical'] == c]
    fig = px.scatter(x=df2['Start_Time'], y=df2['Volume'], title=c, labels={'x': 'Date', 'y': 'Value'},
                  color=df2['Bath'],size_max=1)
    fig.update_xaxes(type='date',dtick="M1",tickformat="%b\n%Y")
    figs.append(fig)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='ATP Dispense'),

    # Row 1: Scatter plot 1
    html.Div([
        dcc.Graph(id='scatter-plot-1', figure=figs[0])
    ]),

    # Row 2: Scatter plot 2
    html.Div([
        dcc.Graph(id='scatter-plot-2', figure=figs[1])
    ]),

    # Row 3: Scatter plot 3
    html.Div([
        dcc.Graph(id='scatter-plot-3', figure=figs[2])
    ]),

    # Row 4: Scatter plot 4
    html.Div([
        dcc.Graph(id='scatter-plot-4', figure=figs[3])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
