import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from read_data import read_data
from write_data import write_data
from predictions_plot import predict_plots
import dash_dangerously_set_inner_html

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

pio.templates.default = "plotly_dark"

df = read_data()
# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('MarsWeather', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/tangcc35/DATA1050_DanTheBest'),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    
    # TODO: Change description markdown below
    return html.Div(children=[dcc.Markdown('''
        # Why Mars
        Mars preserves the record of its formation and can give us insight into how the terrestrial planets formed. 
        It is the perfect laboratory to study the formation and evolution of rocky planets. In this project, we focus on InSight, 
        a mission conducted by NASA to study the crust, mantle, and core of Mars. We collect the data of daily weather measurements 
        (temperature, pressure) on the surface of Mars at Elysium Planitia, a flat, smooth plain near Mars’ equator.

        ### Our Goals
        Given the historical data of weather on Mars, we want to be able to predict the atmosphere temperature and pressure 1 to 3 days 
        from now. At the end of the project, we are expected to gain insights into the weather patterns of Mars and to generate predictions 
        of the weather on Mars to provide more convenience for astronauts, detectors and astronomical research.

        ### Data Source
        We use API to collect data of the weather in the last 7 Sols (unit of Martian Day) on Mars from the [website](https://api.nasa.gov/). 
        For each day, the variables we concentrate on are the maximum temperature, the minimum temperature, the average atmospheric pressure, 
        the wind direction, and the horizontal wind speed. The data source updates once per day. Summary of the data is below:
        **updates every 24 hours 37 minutes**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

def what_if_description():
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        # TODO: change the articles below
        dcc.Markdown('''
        # Predictions and Results:
        We use vector autoregression to make the predictions. Each of the graph includes the historical data and the prediction of 
        the max temperature, the minimum temperature, and the average atmospheric pressure respectively. 
        The solid line records the historical data, while the dashed line shows the predictions. 
        We can also change the prediction interval by moving the slider horizontally. 
        Another thing we need to notice is that the band around the dashed line presents the 95% confidence interval of the predictions. 
        It gets wider as there exists more uncertainty into the farther future.

        # Visualization
        We use a rose chart to present the wind direction and the number of times it blows for each direction on a given day. 
        The degree of an angle is the direction from which the wind blows to. The numbers on the inner circles show the number of 
        times the wind blows in the corresponding directions. We can move the slider to switch to the day we are curious of.
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def what_if_tool():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[

        html.Div(children=[dcc.Graph(id='wind-rose-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("Wind Rose Days Before", style={'marginTop': '2rem'}),

            html.Div(children=[
                dcc.Slider(id='wind-rose-slider', min=int(df['sol_day'][0]), max=int(df['sol_day'][6]), value = int(df['sol_day'][0]), step=1, 
                            marks={df['sol_day'][i] :df['sol_day'][i] for i in [0,1,2,3,4,5,6]})
            ], style={'marginTop': '3rem'})
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),

        html.Div(children=[
            html.H5("Weather Prediction", style={'marginTop': '2rem'}),
            html.H5("Days Ahead", style={'marginTop': '2rem'}),

            html.Div(children=[
                dcc.Slider(id='predictor-slider', min=0, max=5, value = 1, step=1,
                            marks={str(i): str(i) for i in [0,1,2,3,4,5]})
            ], style={'marginTop': '3rem'}),
        ], className='row eleven columns'),
        #className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}

        html.Div(children=[dcc.Graph(id='predictor-figure')], className='nine columns'),

    ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        # TODO: change the articles below
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')

def summary_plot():
    """
    Summary plot for weather on Mars in the past seven days
    """
    return html.Div(children=[
        dash_dangerously_set_inner_html.DangerouslySetInnerHTML("""
    <iframe src='https://mars.nasa.gov/layout/embed/image/insightweather/' 
    width='1040' height='610'  scrolling='no' frameborder='0'></iframe>
    """)], style={'paddingLeft': '5%'})


# Sequentially add page components to the app's layout
app.layout = html.Div([
    page_header(),
    html.Hr(),
    description(),
    summary_plot(),
    what_if_description(),
    what_if_tool(),
    architecture_summary(),
], className='row', id='content')


# Defines the dependencies of interactive components

@app.callback(
    dash.dependencies.Output('predictor-figure', 'figure'),
    [dash.dependencies.Input('predictor-slider', 'value')])
def prediction(step):
    return predict_plots(step, df)


_what_if_data_cache = None


@app.callback(
    dash.dependencies.Output('wind-rose-figure', 'figure'),
    [dash.dependencies.Input('wind-rose-slider', 'value')])
def wind_rose(day):
    df = read_data()
    df_wind = pd.DataFrame.from_dict(df["wind"][df["sol_day"] == str(day)].values[0], orient='index')
    fig = px.bar_polar(df_wind, r="ct", theta="compass_degrees",  
                       color_discrete_sequence= px.colors.sequential.Plasma[-2::-1], 
                       width=600, height=600)
    fig.update_layout(
        title={
            'text': f"Wind Rose Chart of Sol Day {day}",
            'y':0.98,
            'x':0.52,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor='#23272c',
        paper_bgcolor='#23272c')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
