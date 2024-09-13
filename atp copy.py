import pandas as pd
import numpy as np
from datetime import datetime

# Create the initial DataFrame
data = {
    'Start_Time': ['09/12/2024 08:00:00 AM', '09/12/2024 09:00:00 AM', '09/12/2024 10:00:00 AM', '09/12/2024 11:00:00 AM'],
    'Batch_ID': [101, 102, 103, 104],
    'Phase': ['Phase1', 'Phase2', 'Phase1', 'Phase3'],
    'TargetVol_(mL)': [5000, 7000, 6000, 8000],
    'Volume': [4800, 6900, 5800, 7800],
    'Station': ['Station1', 'Station2', 'Station1', 'Station3'],
    'Chemical': ['ChemicalA', 'ChemicalB', 'ChemicalA', 'ChemicalC'],
    'Bath': ['Bath1', 'Bath2', 'Bath1', 'Bath3']
}

df = pd.DataFrame(data)
# LOAD CSV
df = pd.read_csv('atp.csv'); 

# Convert Start_Time to datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %I:%M:%S %p')

# Convert TargetVol_(mL) and Volume to numeric
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'])
df['Volume'] = pd.to_numeric(df['Volume'])

# Remove rows where TargetVol_(mL) < 3100
df = df[df['TargetVol_(mL)'] >= 3100]

# Create lists of unique values
baths = df['Bath'].unique()
chemicals = df['Chemical'].unique()
stations = df['Station'].unique()

# Derive the summary table
df_limits = df.groupby('Chemical')['TargetVol_(mL)'].max().reset_index()
df_limits['UCL'] = df_limits['TargetVol_(mL)'] + 300
df_limits['LCL'] = df_limits['TargetVol_(mL)'] - 300


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = dash.Dash(__name__)

# Create subplots for the app
def create_subplots():
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=[f'Plot {i+1}' for i in range(4)])
    return fig

# Generate figures for each tab
def generate_figures(df, df_limits):
    # First tab: Run Charts
    fig_run_charts = create_subplots()
    for idx, bath in enumerate(df['Bath'].unique()):
        df_bath = df[df['Bath'] == bath]
        fig_run_charts.add_trace(
            go.Scatter(x=df_bath['Start_Time'], y=df_bath['Volume'], mode='lines', name=bath),
            row=1, col=1+idx
        )
        for chemical in df['Chemical'].unique():
            target_vol = df_limits[df_limits['Chemical'] == chemical]['TargetVol_(mL)'].values[0]
            fig_run_charts.add_trace(
                go.Scatter(x=df_bath['Start_Time'], y=[target_vol]*len(df_bath), mode='lines', line=dict(color='black'), name=f'TargetVol_{chemical}'),
                row=idx+1, col=1
            )
    
    # Second tab: Box plots
    fig_box_plots = go.Figure()
    for bath in baths:
        df_bath = df[df['Bath'] == bath]
        fig_box_plots.add_trace(
            go.Box(y=df_bath['Volume'], name=bath)
        )
    
    # Third tab: Scatter plots
    fig_scatter_plots = create_subplots()
    for idx, chemical in enumerate(df['Chemical'].unique()):
        df_chemical = df[df['Chemical'] == chemical]
        fig_scatter_plots.add_trace(
            go.Scatter(x=df_chemical['Start_Time'], y=df_chemical['Volume'], mode='markers', name=chemical),
            row=idx+1, col=1
        )
        target_vol = df_limits[df_limits['Chemical'] == chemical]['TargetVol_(mL)'].values[0]
        fig_scatter_plots.add_trace(
            go.Scatter(x=df_chemical['Start_Time'], y=[target_vol]*len(df_chemical), mode='lines', line=dict(color='black'), name=f'TargetVol_{chemical}'),
            row=idx+1, col=1
        )
    
    return fig_run_charts, fig_box_plots, fig_scatter_plots

fig_run_charts, fig_box_plots, fig_scatter_plots = generate_figures(df, df_limits)

# App layout
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Run Charts', children=[
            html.Div([
                dcc.Graph(figure=fig_run_charts)
            ])
        ]),
        dcc.Tab(label='Box Plots', children=[
            html.Div([
                dcc.Graph(figure=fig_box_plots)
            ])
        ]),
        dcc.Tab(label='Scatter Plots', children=[
            html.Div([
                dcc.Graph(figure=fig_scatter_plots)
            ])
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)