import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample dataset
# df = px.data.gapminder()
df =pd.read_csv('atp.csv')

df = df[df['Start_Time'] > '1/1/2024']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("ATP Dispense History"),
    
    html.Label("Select a Continent:"),
    dcc.Dropdown(
        id='continent-dropdown',
        # options=[{'label': c, 'value': c} for c in df['Chemical'].unique()],
        value='Water'
    ),
    
    dcc.Graph(id='graph'),
    
    html.Label("Select X-axis:"),
    dcc.Dropdown(
        id='xaxis-dropdown',
        # options=[{'label': i, 'value': i} for i in ['Start_Time', 'Start_Time']],
        value='Start_Time'
    )
])

# Define the callback for interactivity
@app.callback(
    Output('graph', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('xaxis-dropdown', 'value')]
)
def update_graph(selected_continent):
    # filtered_df = df[df['continent'] == selected_continent]
    fig = px.scatter(df, 
                    #  x=selected_xaxis, 
                     x='Start_Time',
                     y='Volume', 
                    #  size='pop', 
                    #  color='Bath',
                    #  hover_name='Bath'
                    #  log_x=True,
                    
                    #  size_max=60,
                    #  title=f"Volume vs {selected_xaxis.capitalize()} in {selected_continent}")
                    title='ATP Chart')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
