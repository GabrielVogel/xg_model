import pandas as pd
from ast import literal_eval
from os import listdir
from xg.constants import FEET
def read_file(path):
    df_shots = pd.read_csv(path)
    df_shots['shot_freeze_frame_shot'] = df_shots['shot_freeze_frame_shot'].apply(literal_eval)
    df_shots['location_shot'] = df_shots['location_shot'].apply(literal_eval)
    return df_shots

def find_gk(shot_freeze_frame):
    
    for player in shot_freeze_frame:
        if (player['position']['name'] == "Goalkeeper") and (~player['teammate']):
            return player
    return "No GK"

def format_freeze_data(freeze_og):
    freeze = freeze_og.copy()
    freeze['isGoalkeeper'] = freeze['position'].apply(lambda x : x['name'] == 'Goalkeeper')
    freeze['x'] = freeze['location'].apply(lambda x : x[0])
    freeze['y'] = freeze['location'].apply(lambda x : x[1])
    return freeze
def read_all_files(path='Data'):
    shots_ = pd.DataFrame()
    x = [p for p in listdir(path) if p[:-4] != 'json']
    for f in x:
        print(f"Reading {f}")
        p = f"{path}/{f}"
        shots = read_file(p)
        shots_ = pd.concat([shots_,shots])
    return shots_
    
def get_main_foot(data):
    
    foot = data[data['shot_body_part_shot'].isin(FEET)]
    p = foot.groupby("player_shot").agg(main_foot=('shot_body_part_shot',lambda x: x.value_counts().idxmax()))
    return p


def read_main_foot_data(path="Output/main_foot.json"):
    
    return pd.read_json(path).T.to_dict()['main_foot']

def create_position_map():
    position_map = {'GK':['Goalkeeper'],
                    'DEF':['Right Back','Right Center Back','Center Back','Left Center Back','Left Back','Right Wing Back','Left Wing Back'],
                    'MF':['Left Defensive Midfield','Right Midfield','Right Center Midfield','Center Midfield','Left Center Midfield','Left Midfield','Center Defensive Midfield','Right Attacking Midfield',
                        'Center Attacking Midfield','Left Attacking Midfield','Right Defensive Midfield'],
                    'ATK':['Right Wing','Left Wing','Right Center Forward','Striker','Left Center Forward','Secondary Striker','Center Forward']
                        }
    new_position_map = {}
    for key in position_map:
        for p in position_map[key]:
            new_position_map[p] = key
    return new_position_map