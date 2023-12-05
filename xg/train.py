from sklearn.model_selection import cross_val_predict
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.metrics import brier_score_loss
import pandas as pd
import os
import argparse
from joblib import dump
parser = argparse.ArgumentParser()
parser.add_argument("--feature_set")
parser.add_argument("--run_statsbomb")
parser.add_argument("--train_model")


args = parser.parse_args()

def read_train_data(path='../Output/Train.csv'):
    return pd.read_csv(path)

def calculate_metric(ytrue,yproba):
    """Given ytrue and yproba, calculate Brier Score"""
    
    return brier_score_loss(ytrue,yproba)

def cross_val_predict_model(X,y):
    """Given X and y, cross_val_predict the data and returns brier_score_loss output."""
    clf = ExplainableBoostingClassifier(interactions=0)
    preds = cross_val_predict(clf,X,y,method='predict_proba')[:,1]
    metric = calculate_metric(y,preds)
    return metric

def read_feature_files(name):
    
    pname = f'../Features/{name}.txt'
    f = open(pname,mode='r').read().splitlines() 
    return f

def select_columns(df,fname):
    cols = read_feature_files(fname)
    return df[cols]

def X_y(df):
    dfc = df.copy()
    y = dfc.pop('goal')
    return dfc,y


def train_full_model(X,y,fname):
    clf = ExplainableBoostingClassifier(interactions=0)
    clf.fit(X,y)
    p = f"../Models/{fname}.joblib"
    dump(clf,p)

def write_to_log_file(fname,score,path='../Output/model_results.json'):
    
    if os.path.isfile(path):
        log = pd.read_json(path,typ='series', orient='index')
        log[fname] = score
        log.to_json(path)
    else:
        d = {fname:score}
        pd.Series(d).to_json(path)


fname = args.feature_set
run_statsbomb_xg = args.run_statsbomb
train_b = args.train_model
df = read_train_data()
X,y = X_y(df)
Xc = select_columns(X,fname)
print("Generating cross validation scores predictions...")
metric = cross_val_predict_model(Xc,y)
print("Predictions done!")
write_to_log_file(fname,metric)
print("Predictions evaluations added to log file!")
if run_statsbomb_xg:
    sxg = X['shot_statsbomb_xg_shot']
    metric = brier_score_loss(y,sxg)
    write_to_log_file('statsbomb_xg',metric)
if train_b:
    print("Training full model")
    train_full_model(Xc,y,fname)
    print("Training done!")

