import requests
import json
import numpy as np
import pandas as pd
import logging
import utils
import sched
import time
import pymongo


logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')

# Request data from api
key = "j8jSUUXusA5glsJa3q5bQaDad6sE4H2u9K5rFbST"
requested = requests.get(f"https://api.nasa.gov/insight_weather/?api_key={key}&feedtype=json&ver=1.0").text
requested = json.loads(requested)
DOWNLOAD_PERIOD = 10    # 30 seconds
counting = 1

# Get all the sol_days from this request
main_keys = requested['sol_keys']


def valid_check(subject, index):
    """Check if data is valid"""
    return requested['validity_checks'][index][subject]['valid']


def write_data():
    """Write data into mongodb"""
    # write save useful data into dataframe, dummy is -1
    df_requested = {"sol_day": [-1], "date": [-1], "min_temp": [-1], "max_temp": [-1], "pressure": [-1], "wind": [-1]}
    for i in main_keys:
        df_requested["sol_day"].append(i)
        df_requested["date"].append(requested[i]['Last_UTC'])
        df_requested["min_temp"].append(
            requested[i]['AT']["mn"] if valid_check('AT', i) else df_requested["min_temp"][-1])
        df_requested["max_temp"].append(
            requested[i]['AT']["mx"] if valid_check('AT', i) else df_requested["max_temp"][-1])
        df_requested["pressure"].append(
            requested[i]['PRE']["av"] if valid_check('PRE', i) else df_requested["pressure"][-1])
        df_requested["wind"].append(requested[i]["WD"] if valid_check('WD', i) else df_requested["wind"][-1])
    df_requested = pd.DataFrame(df_requested)
    df_requested.drop(0, inplace=True)    # drop dummy
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
                
                
def main_loop(timeout = DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        write_data()
        scheduler.enter(timeout, 1, _worker)

    scheduler.enter(0, 1, _worker) # start the first event
    scheduler.run(blocking=True)

    
if __name__ == '__main__':
    main_loop()
