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
        # Energy Planner
        As of today, 138 cities in the U.S. have formally announced 100% renewable energy goals or
        targets, while others are actively considering similar goals. Despite ambition and progress,
        conversion towards renewable energy remains challenging.

        Wind and solar power are becoming more cost effective, but they will always be unreliable
        and intermittent sources of energy. They follow weather patterns with potential for lots of
        variability. Solar power starts to die away right at sunset, when one of the two daily peaks
        arrives (see orange curve for load).

        **Energy Planner is a "What-If" tool to assist making power conversion plans.**
        It can be used to explore load satisfiability under different power contribution with 
        near-real-time energy production & consumption data.

        ### Data Source
        Energy Planner utilizes near-real-time energy production & consumption data from [BPA 
        Balancing Authority](https://www.bpa.gov/news/AboutUs/Pages/default.aspx).
        The [data source](https://transmission.bpa.gov/business/operations/Wind/baltwg.aspx) 
        **updates every 5 minutes**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")

def what_if_description():
    """
    Returns description of "What-If" - the interactive component
    """
    return html.Div(children=[
        # TODO: change the articles below
        dcc.Markdown('''
        # " What If "
        So far, BPA has been relying on hydro power to balance the demand and supply of power. 
        Could our city survive an outage of hydro power and use up-scaled wind power as an
        alternative? Find below **what would happen with 2.5x wind power and no hydro power at 
        all**.   
        Feel free to try out more combinations with the sliders. For the clarity of demo code,
        only two sliders are included here. A fully-functioning What-If tool should support
        playing with other interesting aspects of the problem (e.g. instability of load).
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
