# -*- coding: utf-8 -*-
"""IPL Score Predictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gymgX_NLUpU5JdLQH_nDHH1eAVG0OT3A
"""

import pandas as pd
import numpy as np

ipl = pd.read_csv('IPL_ball_by_ball_updated.csv')

ipl.info()

ipl.head(5)

ipl['batting_team'].unique()

ipl['bowling_team'].unique()

ipl['venue'].value_counts()

#Copying actual dataset
df = ipl.copy()

df['venue'] = df['venue'].str.split(",", n=1, expand = True).get(0)

df['venue'].replace("M.Chinnaswamy Stadium", "M Chinnaswamy Stadium", inplace = True)
df['venue'].replace("Punjab Cricket Association Stadium", "Punjab Cricket Association IS Bindra Stadium", inplace = True)
df['venue'].replace("Sardar Patel Stadium", "Narendra Modi Stadium", inplace = True)
df['venue'].replace("Zayed Cricket Stadium", "Sheikh Zayed Stadium", inplace = True)
df['venue'].replace("Feroz Shah Kotla", "Arun Jaitley Stadium", inplace = True)

df['venue'].value_counts()

df['batting_team'].replace("Kings XI Punjab", "Punjab Kings", inplace = True)
df['bowling_team'].replace("Kings XI Punjab", "Punjab Kings", inplace = True)

df['batting_team'].replace("Rising Pune Supergiant", "Rising Pune Supergiants", inplace = True)
df['bowling_team'].replace("Rising Pune Supergiant", "Rising Pune Supergiants", inplace = True)
df['batting_team'].replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
df['bowling_team'].replace("Delhi Daredevils", "Delhi Capitals", inplace = True)
df['batting_team'].replace("Gujarat Lions", "Gujarat Titans", inplace = True)
df['bowling_team'].replace("Gujarat Lions", "Gujarat Titans", inplace = True)

df['batting_team'].value_counts()

df['bowling_team'].value_counts()

df.columns

"""For  score calulation we don't need how the extra run scored so we can drop those columns : 'wides', 'noballs', 'byes', 'legbyes', 'penalty', 'wicket_type','other_wicket_type', 'other_player_dismissed'"""

df = df.drop(['start_date','striker','bowler', 'non_striker','wides', 'noballs', 'byes', 'legbyes', 'penalty', 'wicket_type','other_wicket_type', 'other_player_dismissed'], axis = 1)

df.head(5)

team_runs = df.groupby(['match_id','batting_team', 'innings'])[['runs_off_bat', 'extras']].sum()
team_runs

# calculate the total runs by adding the runs_scored and extras columns
team_runs['total_runs'] = team_runs['runs_off_bat'] + team_runs['extras']
team_runs = team_runs.reset_index()
team_runs

# Merge the total_runs column to df_main
team_runs = team_runs.groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
df = pd.merge(df, team_runs, on=['match_id', 'batting_team'])

df.info()

df['runs'] = df['runs_off_bat'] + df['extras']
df['current_score'] = df.groupby(['match_id', 'batting_team'])['runs'].cumsum()

df['player_dismissed'] = df['player_dismissed'].apply(lambda x:0 if pd.isna(x) else 1)
df['player_dismissed'] = df['player_dismissed'].astype('int')
df['wickets'] = df.groupby(['match_id','batting_team']).cumsum()['player_dismissed']

df['over'] = df['ball'].apply(lambda x: str(x).split(".")[0]).astype('int')
df['over_ball'] = df['ball'].apply(lambda x: str(x).split(".")[1]).astype('int')
df['balls'] = (df['over'])*6 + df['over_ball']

df.head(5)

df['crr'] = round((df['current_score'])/(df['over']+(df['over_ball']/6)),2)

groups = df.groupby('match_id')
match_id = df['match_id'].unique()
last_5over_runs = []
for id in match_id:
  last_5over_runs.extend(groups.get_group(id).rolling(window=30).sum()['runs'].values.tolist())

df['last_5over_runs'] = last_5over_runs
df

df['last_5over_runs'].fillna(0, inplace=True)

df.columns

"""Improtant columns we needed are :- Match id, Season, Venue, Innings, Batting and Bowling team, total_runs, current score, wickets, balls, crr, last 5 over runs"""

# Taking only 8 seasons for testing the model accuracy
final_df = df[df['season'] >= 2015]

final_df = final_df[['batting_team','bowling_team','venue','innings','current_score','wickets','over','over_ball','crr','last_5over_runs','total_runs']]
final_df

final_df.isnull().sum()

final_df['venue'].unique()

final_df['batting_team'].unique()

"""## Model Building"""

#Spliting dataset into train and test data
X = final_df.drop(columns=['total_runs'])
y = final_df['total_runs']
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0)

X_train.shape, X_test.shape

y_train.shape, y_test.shape

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score,mean_absolute_error

trf = ColumnTransformer([
    ('trf',OneHotEncoder(sparse_output=False,drop='first'),['batting_team','bowling_team','venue'])
]
,remainder='passthrough')

"""# Model"""

#XGBoost Regression
from xgboost import XGBRegressor
xgb = XGBRegressor(n_estimators=800,learning_rate=0.08,max_depth=12,random_state=0)
xgb.fit(X_train_scaled,y_train)
y_xgb=xgb.predict(X_test_scaled)
print(r2_score(y_test,y_xgb))
print(mean_absolute_error(y_test,y_xgb))

"""800,0.2,12---->96, 2.8

800,0.1,15---->96.2, 2.6

800,0.08,15----> 96.4,2.5

900,0.2,12----->96, 2.82

Making a pipeline for model
"""

pl = Pipeline(steps=[
    ('step1',trf),
    ('step2',StandardScaler()),
    ('step3',XGBRegressor(n_estimators=800,learning_rate=0.08,max_depth=15,random_state=1))
])

pl.fit(X_train,y_train)
y_pred = pl.predict(X_test)
print(r2_score(y_test,y_pred))
print(mean_absolute_error(y_test,y_pred))

import pickle
pickle.dump(pl,open('pl.pkl','wb'))