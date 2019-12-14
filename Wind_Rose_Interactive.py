import dash
import dash_html_components as html
import dash_core_components as dcc
from read_data import read_data
from write_data import write_data
import numpy as np
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

write_data()
df = read_data()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='what-if-figure'),
    dcc.Slider(id='wind-rose-slider', min=int(df['sol_day'][0]), max=int(df['sol_day'][6]), value = int(df['sol_day'][0]), step=1, 
                marks={df['sol_day'][i] :df['sol_day'][i] for i in [0,1,2,3,4,5,6]})
])


@app.callback(
    dash.dependencies.Output('what-if-figure', 'figure'),
    [dash.dependencies.Input('wind-rose-slider', 'value')])
def wind_rose(day):
    cond = df["sol_day"] == str(day)
    wind_data = df["wind"][cond].to_dict()[day % 365]
    df_wind = pd.DataFrame.from_dict(wind_data, orient="index")
    fig = px.bar_polar(df_wind, r="ct", theta="compass_degrees",  
                       color_discrete_sequence= px.colors.sequential.Plasma[-2::-1], 
                       width=600, height=600)
    fig.update_layout(
        title={
            'text': f"Wind Rose Chart of Sol Day {str(day)}",
            'y':0.98,
            'x':0.53,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)