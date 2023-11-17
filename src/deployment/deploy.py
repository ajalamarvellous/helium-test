# import important libraries
from fastapi import FastAPI
import pickle
import pandas as pd
from typing import List, Dict

# create an instance of FastAPI
MODEL_NAME = "Random Forest"
app = FastAPI()
encoder = pickle.load(open("../../models/encoder.pkl", "rb"))
model = pickle.load(open(f"../../models/{MODEL_NAME}.pkl", "rb"))

# define a / endpoint
@app.get("/")
def index():
    return {"message": "Hello welcome to this resources prediction app! \
            we'll be predicting the number of patients you'll probably \
            be seeing in your facility given the data you provide."}

# define a /prediction endpoint
@app.post("/prediction")
def prediction(data: dict):
    data = pd.DataFrame.from_dict(data)
    data = preprocess_data(data)
    prediction = model.predict(data)
    return prediction

def preprocess_data(df: pd.DataFrame):
    df["institution_id"] = encoder.transform(df["institution_id"])
    # expanding the time column to day, week, day of the week and month
    df["day"] = df.inserted_at.dt.day
    df["week"] = df.inserted_at.dt.week
    df["day_of_the_week"] = df.inserted_at.dt.dayofweek
    df["month"] = df.inserted_at.dt.month
    return df

# NOTE: this demo is for implementation purposes only, it is not a production ready app
# to deal with security, there with be a need for either a token (jwt) or an authentication
# process to ensure that only authorized users can access the app and data security and privacy
# is maintained. Both methods can also be implemented with FastAPI

# also, the model performance can be monitored using a combination of tools like MLFlow, EvidentlyAI and 
# Prometheus. This will ensure that the model performance is monitored and the model is retrained when necessary
# to ensure that the model performance is not degraded. Also, change in data distribution can be detected and
# monitored using tool such as cleanlab to also measure data drift over time.