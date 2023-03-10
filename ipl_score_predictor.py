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

ipl.head(100)

ipl['batting_team'].unique()

ipl['venue'].value_counts()

ipl['batting_team'].value_counts()

#Making copy of actual file
df = ipl.copy()

df['venue'] = df['venue'].str.split(",", n=1, expand = True).get(0)

df['venue'].replace("M.Chinnaswamy Stadium", "M Chinnaswamy Stadium", inplace = True)

df['venue'].replace("Punjab Cricket Association Stadium", "Punjab Cricket Association IS Bindra Stadium", inplace = True)

df['venue'].value_counts()

df['batting_team'].replace("Punjab Kings", "Kings XI Punjab", inplace = True)

df['batting_team'].value_counts()

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

df = df[df['season'] != 2022]

df.tail(2)

df['runs'] = df['runs_off_bat'] + df['extras']
df['current_score'] = df.groupby(['match_id', 'batting_team'])['runs'].cumsum()

df['player_dismissed'] = df['player_dismissed'].apply(lambda x:0 if pd.isna(x) else 1)
df['player_dismissed'] = df['player_dismissed'].astype('int')
df['wickets'] = df.groupby(['match_id','batting_team']).cumsum()['player_dismissed']

df['over'] = df['ball'].apply(lambda x: str(x).split(".")[0]).astype('int')
df['over_ball'] = df['ball'].apply(lambda x: str(x).split(".")[1]).astype('int')
df['balls'] = (df['over'])*6 + df['over_ball']

df.head(5)

df['crr'] = (df['current_score']*6)/df['balls']

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

final_df = df[['venue','innings','batting_team','bowling_team','current_score','wickets','over','over_ball','crr','last_5over_runs','total_runs']]
final_df

final_df.isnull().sum()

final_df = final_df.sample(final_df.shape[0])
final_df

"""## Model Building"""

#Spliting dataset into train and test data
X = final_df.drop(columns=['total_runs'])
y = final_df['total_runs']
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.2, random_state = 0)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score,mean_absolute_error

trf = ColumnTransformer([
    ('trf',OneHotEncoder(sparse=False,drop='first'),['batting_team','bowling_team','venue'])
]
,remainder='passthrough')

pl = Pipeline(steps=[
    ('step1',trf),
    ('step2',StandardScaler()),
    ('step3',XGBRegressor(n_estimators=800,learning_rate=0.3,max_depth=10,random_state=1))
])

pl.fit(X_train,y_train)
y_pred = pl.predict(X_test)
print(r2_score(y_test,y_pred))
print(mean_absolute_error(y_test,y_pred))

import pickle
pickle.dump(pl,open('pl.pkl','wb'))