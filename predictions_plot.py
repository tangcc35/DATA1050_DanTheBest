import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def predict_plots(step, df):
    main_keys = df['sol_day'].values
    model = pickle.load(open("VAR_model_2.sav", "rb"))
    sol_days_pred = [int(main_keys[-1]) + i for i in range(0, step + 1)]    # Sol days to predict
    pred = model.forecast_interval(df.iloc[-3:, 2:5].values, step)    # Predictions needed
    prev_max_temp = list(df["max_temp"])    # Previous max temperatures
    max_temp_dic = {}    # Record predicted max temperature and confidence intervals
    
    # set up 
    fig = make_subplots(rows=3, cols=1, subplot_titles=("Max Temperature", "Min Temperature", "Average Pressure",))
    
    # plot max temperature
    prev_max_temp = list(df["max_temp"])    # Previous max temperatures
    max_temp_dic = {}    # Record predicted max temperature and confidence intervals
    for i in range(0, 3):
        max_temp_dic['temp_exp'] = [prev_max_temp[-1]] + [i[1] for i in pred[0]]
        max_temp_dic['temp_lower'] = [prev_max_temp[-1]] +  [i[1] for i in pred[1]]
        max_temp_dic['temp_upper'] = [prev_max_temp[-1]] +  [i[1] for i in pred[2]]
    fig.add_trace(go.Scatter(x=df['sol_day'], y=prev_max_temp,
                         mode='lines', 
                         name='Known Max Temperature', 
                         line_color='rgb(255, 102, 163)',
                         showlegend=False, 
                         ), row=1, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=max_temp_dic['temp_exp'],
                         mode='lines', 
                         line=dict(dash='dash'), 
                         line_color='rgb(255, 102, 163)', 
                         name='Expected Max Temperature'), row=1, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=max_temp_dic['temp_upper'],
                         mode='lines',
                         name='Interval of Max Temperature', 
                         line_color='rgba(255, 102, 163, 0.2)', 
                         showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=max_temp_dic['temp_lower'],
                         mode='lines',
                         name='Interval of Max Temperature', 
                         fill='tonexty', 
                         line_color='rgba(255, 102, 163, 0.2)', 
                         fillcolor='rgba(255, 102, 163, 0.2)'), row=1, col=1)
    fig.update_xaxes(title_text="Sol Day", row=1, col=1)
    fig.update_yaxes(title_text="Degrees of Celcius", row=1, col=1)
    
    # plot min temperature
    prev_min_temp = list(df["min_temp"])    # Previous min temperatures
    min_temp_dic = {}    # Record predicted min temperature and confidence intervals
    for i in range(0, 3):
        min_temp_dic['temp_exp'] = [prev_min_temp[-1]] + [i[0] for i in pred[0]]
        min_temp_dic['temp_lower'] = [prev_min_temp[-1]] +  [i[0] for i in pred[1]]
        min_temp_dic['temp_upper'] = [prev_min_temp[-1]] +  [i[0] for i in pred[2]]
    fig.add_trace(go.Scatter(x=df['sol_day'], y=prev_min_temp,
                         mode='lines', 
                         name='Known Max Temperature', 
                         line_color='rgb(102, 181, 255)',
                         showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=min_temp_dic['temp_exp'],
                         mode='lines', 
                         line=dict(dash='dash'), 
                         line_color='rgb(102, 181, 255)', 
                         name='Expected Min Temperature'), row=2, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=min_temp_dic['temp_upper'],
                         mode='lines',
                         name='Interval of Min Temperature', 
                         line_color='rgba(102, 181, 255, 0.2)', 
                         showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=min_temp_dic['temp_lower'],
                         mode='lines',
                         name='Interval of Min Temperature', 
                         fill='tonexty', 
                         line_color='rgba(102, 181, 255, 0.2)', 
                         fillcolor='rgba(102, 181, 255, 0.2)'), row=2, col=1)
    fig.update_xaxes(title_text="Sol Day", row=2, col=1)
    fig.update_yaxes(title_text="Degrees of Celcius", row=2, col=1)
    
    # plot avg temperature
    prev_ps = list(df['pressure'])    # Previous max temperatures
    ps_dic = {}    # Record predicted max temperature and confidence intervals
    for i in range(0, 3):
        ps_dic['ps_exp'] = [prev_ps[-1]] + [i[2] for i in pred[0]]
        ps_dic['ps_lower'] = [prev_ps[-1]] +  [i[2] for i in pred[1]]
        ps_dic['ps_upper'] = [prev_ps[-1]] +  [i[2] for i in pred[2]]
    fig.add_trace(go.Scatter(x=df['sol_day'], y=prev_ps,
                         mode='lines', 
                         name='Known Avg Pressure', 
                         line_color='rgb(102, 255, 179)',
                         showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=ps_dic['ps_exp'],
                         mode='lines', 
                         line=dict(dash='dash'), 
                         line_color='rgb(102, 255, 179)', 
                         name='Expected Avg Pressure'), row=3, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=ps_dic['ps_upper'],
                         mode='lines',
                         name='Interval of Avg Pressure', 
                         line_color='rgba(102, 255, 179, 0.2)', 
                         showlegend=False), row=3, col=1)
    fig.add_trace(go.Scatter(x=sol_days_pred, y=ps_dic['ps_lower'],
                         mode='lines',
                         name='Interval of Avg Pressure', 
                         fill='tonexty', 
                         line_color='rgba(102, 255, 179, 0.2)', 
                         fillcolor='rgba(102, 255, 179, 0.2)'), row=3, col=1)
    fig.update_xaxes(title_text="Sol Day", row=3, col=1)
    fig.update_yaxes(title_text="Pascal", row=3, col=1)
    
    fig.update_layout(width=1500, height=900)
    
    return fig
 