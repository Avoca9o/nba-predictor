import pandas as pd
import pickle

abbr_id_mapper = None
current_data = None
predictor = None

with open('abbr_id_mapper.csv', 'r') as f:
    abbr_id_mapper = pd.read_csv(f)
    abbr_id_mapper = dict(zip(abbr_id_mapper['abbreviation'], abbr_id_mapper['id']))

with open('current_data.csv', 'r') as f:
    current_data = pd.read_csv(f)

with open('predictor.pkl', 'rb') as f:
    predictor = pickle.load(f)

def get_prediction(data: dict):
    team_abbreviation_home = data['home_team_abbreaviation']
    team_abbreviation_away = data['away_team_abbreaviation']

    print(abbr_id_mapper.keys())

    team_id_home = abbr_id_mapper[team_abbreviation_home]
    team_id_away = abbr_id_mapper[team_abbreviation_away]

    mask = (current_data['home_team_id'] == team_id_home) & (current_data['away_team_id'] == team_id_away)
    if mask.any():
        last_row = current_data[mask].iloc[[-1]]
        last_row = last_row.drop(columns=['home_team_id', 'away_team_id'])
        prediction = predictor.predict(last_row)
        return int(prediction)
    else:
        return -1
