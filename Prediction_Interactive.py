import dash
import dash_html_components as html
import dash_core_components as dcc
from read_data import read_data
from write_data import write_data
import numpy as np
import plotly.express as px
import pandas as pd
from predictions_plot import predict_plots
from statsmodels.tsa.api import VAR

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

write_data()
df = read_data()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='what-if-figure'),
    dcc.Slider(id='wind-rose-slider', min=0, max=5, value = 1, step=1)
])


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('wind-rose-slider', 'value')])
def prediction(step):
    return predict_plots(step, df)


if __name__ == '__main__':
    app.run_server(debug=True)