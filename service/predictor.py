import random
import pandas as pd
import json
import pickle

preprocessor = None
predictor = None

with open('preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)
with open('predictor.pkl', 'rb') as f:
    predictor = pickle.load(f)

def get_prediction(data: dict):
    columns = data.keys()

    df = pd.DataFrame([data])

    df = preprocessor.transform(df)
    df = pd.DataFrame(df, columns=columns)

    prediction = predictor.predict(df)
    return int(prediction)
