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
    dcc.Graph(id='predictor-figure'),
    dcc.Slider(id='predictor-slider', min=0, max=5, value = 1, step=1,
                marks={str(i): str(i) for i in [0,1,2,3,4,5]})
])


@app.callback(
    dash.dependencies.Output('predictor-figure', 'figure'),
    [dash.dependencies.Input('predictor-slider', 'value')])
def prediction(step):
    print(df['pressure'])
    return predict_plots(step, df)


if __name__ == '__main__':
    app.run_server(debug=True)