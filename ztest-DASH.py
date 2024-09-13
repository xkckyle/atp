import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pickle
import base64

# Load your Plotly chart from a pickle file
def load_plotly_chart_from_pickle(pickle_file):
    with open(pickle_file, 'rb') as file:
        chart = pickle.load(file)
    return chart

# Create a sample plotly chart and save it as a pickle file
# Uncomment the following lines to create a sample chart and pickle it
# df = px.data.iris()
# fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
# with open('chart.pkl', 'wb') as f:
#     pickle.dump(fig, f)

# Encode JPG image
def encode_image(image_file):
    with open(image_file, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode('utf-8')
    return encoded_image

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Plotly Chart', 'value': 'chart'},
            {'label': 'JPG Image', 'value': 'image'}
        ],
        value='chart'
    ),
    html.Div(id='content')
])

@app.callback(
    Output('content', 'children'),
    [Input('dropdown', 'value')]
)
def update_content(selected_option):
    if selected_option == 'chart':
        fig = load_plotly_chart_from_pickle("atp-new.pkl")
        return dcc.Graph(figure=fig)
    elif selected_option == 'image':
        img_src = encode_image('atp-old.jpg')
        return html.Img(src=f'data:image/jpeg;base64,{img_src}', style={'width': '100%', 'height': 'auto'})
    return html.Div('Select an option from the dropdown.')

if __name__ == '__main__':
    app.run_server(debug=True)
