import numpy as np
import pandas as pd
import pymongo



def read_data():
    """Read data from mongodb"""
    client = pymongo.MongoClient()
    db = client.get_database("MarsWeather")
    collection = db.get_collection("DailyWeather")
    df = pd.DataFrame(list(collection.find()))
    return df