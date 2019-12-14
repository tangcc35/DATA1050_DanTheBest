import requests
import json
import numpy as np
import pandas as pd
import logging
import utils
import pymongo



# Request data from api
key = "j8jSUUXusA5glsJa3q5bQaDad6sE4H2u9K5rFbST"
requested = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={key}&feedtype=json&ver=1.0").text
requested = json.loads(requested)
logger = logging.Logger(__name__)


# Get all the sol_days from this request
main_keys = requested['sol_keys']

def write_data():
    """Write data into mongodb"""
    # write save useful data into dataframe
    df_requested = {"sol_day": [], "date": [], "min_temp": [], "max_temp": [], "pressure": [], "wind": []}
    for i in main_keys:
        df_requested["sol_day"].append(i)
        df_requested["date"].append(requested[i]['Last_UTC'])
        df_requested["min_temp"].append(requested[i]['AT']["mn"])
        df_requested["max_temp"].append(requested[i]['AT']["mx"])
        df_requested["pressure"].append(requested[i]['PRE']["av"])
        df_requested["wind"].append(requested[i]["WD"])
    df_requested = pd.DataFrame(df_requested)
    # write to mongodb with dict
    data = df_requested.to_dict(orient='records')
    client = pymongo.MongoClient()
    db = client.get_database("MarsWeather")
    collection = db.get_collection("DailyWeather")
    update_count = 0
    for record in data:
        result = collection.replace_one(
            filter={'sol_day': record['sol_day']},    # locate the document if exists
            replacement=record,                         # latest document
            upsert=True)                                # update if exists, insert if not
        if result.matched_count > 0:
            update_count += 1
    logger.info("rows={}, update={}, ".format(df_requested.shape[0], update_count) +
                "insert={}".format(df_requested.shape[0]-update_count))
    
    
if __name__ == '__main__':
    main_loop()