import pandas as pd
from datetime import datetime

# Create the initial DataFrame
data = {
    'Start_Time': ['09/12/2024 08:00:00 AM', '09/12/2024 09:00:00 AM', '09/12/2024 10:00:00 AM', '09/12/2024 11:00:00 AM'],
    'Batch_ID': [101, 102, 103, 104],
    'Phase': ['Phase1', 'Phase2', 'Phase1', 'Phase3'],
    'TargetVol_(mL)': [3200, 3500, 2900, 4000],
    'Volume': [3100, 3400, 2800, 3900],
    'Station': ['A-1', 'B-2', 'A-1', 'C-3'],
    'Chemical': ['ChemicalA', 'ChemicalB', 'ChemicalA', 'ChemicalC'],
    'Bath': ['A', 'B', 'C', 'D']
}

df = pd.DataFrame(data)
# df = pd.read_csv('atp.csv')  # Uncomment this line if reading from a CSV file

# Convert columns to appropriate types
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'])
df['Volume'] = pd.to_numeric(df['Volume'])
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %I:%M:%S %p')

# Remove rows where TargetVol_(mL) < 3100
df = df[df['TargetVol_(mL)'] >= 3100]

# Create lists of unique Baths, Chemicals, and Stations
bath_list = df['Bath'].unique()
chemical_list = df['Chemical'].unique()
station_list = df['Station'].unique()

# Derive the summary table
df_limits = df.groupby('Chemical')['TargetVol_(mL)'].max().reset_index()
df_limits.rename(columns={'TargetVol_(mL)': 'Max_TargetVol_(mL)'}, inplace=True)
df_limits['UCL'] = df_limits['Max_TargetVol_(mL)'] + 300
df_limits['LCL'] = df_limits['Max_TargetVol_(mL)'] - 300

# Comment out print statements
# print("Original DataFrame:")
# print(df)

# print("\nList of Baths:")
# print(bath_list)

# print("\nList of Chemicals:")
# print(chemical_list)

# print("\nList of Stations:")
# print(station_list)

# print("\nSummary DataFrame:")
# print(df_limits)


from dash import dcc, html, Dash
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Initialize the Dash app
app = Dash(__name__)

# Create line charts for each Bath and Chemical combination
def create_line_charts(df, df_limits):
    fig = make_subplots(rows=len(df['Chemical'].unique()), cols=len(df['Bath'].unique()), 
                        subplot_titles=[f'{chem} - {bath}' for chem in df['Chemical'].unique() for bath in df['Bath'].unique()],
                        shared_xaxes=True, shared_yaxes=True)
    
    chemicals = df['Chemical'].unique()
    baths = df['Bath'].unique()

    for i, chemical in enumerate(chemicals):
        for j, bath in enumerate(baths):
            df_filtered = df[(df['Chemical'] == chemical) & (df['Bath'] == bath)]
            limits = df_limits[df_limits['Chemical'] == chemical].iloc[0]
            fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=df_filtered['Volume'], mode='lines+markers',
                                     name=chemical, marker=dict(size=5), showlegend=(i == 0)),
                          row=i + 1, col=j + 1)
            fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=[limits['Max_TargetVol_(mL)']] * len(df_filtered),
                                     mode='lines', line=dict(color='black', dash='dash'), showlegend=False),
                          row=i + 1, col=j + 1)
            fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=[limits['UCL']] * len(df_filtered),
                                     mode='lines', line=dict(color='red', dash='dash'), showlegend=False),
                          row=i + 1, col=j + 1)
            fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=[limits['LCL']] * len(df_filtered),
                                     mode='lines', line=dict(color='red', dash='dash'), showlegend=False),
                          row=i + 1, col=j + 1)

    fig.update_layout(title_text="ATP Dispense - Run Charts", height=800)
    return fig

def create_box_plots(df):
    fig = make_subplots(rows=1, cols=1)
    
    for chemical in df['Chemical'].unique():
        df_filtered = df[df['Chemical'] == chemical]
        fig.add_trace(go.Box(x=df_filtered['Bath'], y=df_filtered['Volume'], name=chemical,
                             marker=dict(size=5), boxmean='sd'),
                      row=1, col=1)
    
    fig.update_layout(title_text="Volume Distribution by Chemical and Bath")
    return fig

def create_scatter_plots(df, df_limits):
    fig = make_subplots(rows=len(df['Chemical'].unique()), cols=1, shared_xaxes=True, shared_yaxes=True,
                        subplot_titles=[chem for chem in df['Chemical'].unique()])

    for i, chemical in enumerate(df['Chemical'].unique()):
        df_filtered = df[df['Chemical'] == chemical]
        limits = df_limits[df_limits['Chemical'] == chemical].iloc[0]
        fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=df_filtered['Volume'], mode='markers',
                                 marker=dict(size=5, color=bath_list), name=chemical),
                      row=i + 1, col=1)
        fig.add_trace(go.Scatter(x=df_filtered['Start_Time'], y=[limits['Max_TargetVol_(mL)']] * len(df_filtered),
                                 mode='lines', line=dict(color='black', dash='dash'), showlegend=False),
                      row=i + 1, col=1)
    
    fig.update_layout(title_text="Scatter Plots by Chemical", height=800)
    return fig

# Define the layout of the Dash app
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='ATP Dispense - Run Charts', children=[
            dcc.Graph(figure=create_line_charts(df, df_limits))
        ]),
        dcc.Tab(label='Box Plots', children=[
            dcc.Graph(figure=create_box_plots(df))
        ]),
        dcc.Tab(label='Scatter Plots', children=[
            dcc.Graph(figure=create_scatter_plots(df, df_limits))
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)