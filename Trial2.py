from read_data import read_data
from write_data import write_data
import pandas as pd
import plotly.express as px

write_data()
day = 366
df = read_data()
print(df['sol_day'][1])
cond = df["sol_day"] == str(day)
wind_data = df["wind"][cond].to_dict()[day - 365]
df_wind = pd.DataFrame.from_dict(wind_data, orient="index")


fig = px.bar_polar(df_wind, r="ct", theta="compass_degrees",  
                       color_discrete_sequence= px.colors.sequential.Plasma[-2::-1], 
                       width=600, height=600)

fig.update_layout(
        title={
            'text': f"Wind Rose Chart of Sol Day {str(365)}",
            'y':0.98,
            'x':0.53,
            'xanchor': 'center',
            'yanchor': 'top'})
print(fig)