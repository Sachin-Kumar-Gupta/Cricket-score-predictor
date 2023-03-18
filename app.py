import streamlit as st
import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor
import bz2

with bz2.BZ2File('pickle.pkl.bz2', 'r') as f:
    pl = pickle.load(f)

venues = ['Eden Gardens', 'MA Chidambaram Stadium','Maharashtra Cricket Association Stadium', 'Arun Jaitley Stadium','Wankhede Stadium', 'M Chinnaswamy Stadium',
          'Narendra Modi Stadium','Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium','Punjab Cricket Association IS Bindra Stadium','Rajiv Gandhi International Stadium', 'Brabourne Stadium',
          'Shaheed Veer Narayan Singh International Stadium','JSCA International Stadium Complex','Saurashtra Cricket Association Stadium', 'Green Park',
          'Holkar Cricket Stadium', 'Sawai Mansingh Stadium','Sheikh Zayed Stadium', 'Dubai International Cricket Stadium','Sharjah Cricket Stadium']

teams = ['Mumbai Indians', 'Kolkata Knight Riders', 'Chennai Super Kings','Delhi Capitals', 'Rajasthan Royals', 'Punjab Kings','Sunrisers Hyderabad',
         'Royal Challengers Bangalore','Rising Pune Supergiants', 'Gujarat Titans']

overs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
balls = [1,2,3,4,5,6]

st.title('Score Predictor')

col_1, col_2 = st.columns(2)

with col_1:
    batting_team = st.selectbox('Select batting team',sorted(teams))
with col_2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

Venue = st.selectbox('Select city',sorted(venues))

col_3,col_4,col_5,col_6, col_7 = st.columns(5)

with col_3:
    current_score = st.number_input('Current Score', value=0, step=1)
with col_4:
    over = st.selectbox('Overs done(works for over>5)', sorted(overs))
with col_5:
    over_ball = st.selectbox('Ball of the over', sorted(balls))
with col_6:
    wickets = st.number_input('Wickets out')
with col_7:
    innings = st.radio('Inning', [1, 2], index=0)
    
last_5over_runs = st.number_input('Runs scored in last 5 overs')

if st.button('Predict Score'):
    over_done = (over) + (over_ball/6)
    wickets_left = 10 - wickets
    crr = (current_score)/over_done

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'venue': [Venue],
        'innings': [innings],
        'current_score': [current_score],
        'wickets': [wickets],
        'over': [over],
        'over_ball': [over_ball],
        'crr': [crr],
        'last_5over_runs': [last_5over_runs]
    })
    result = pl.predict(input_df)
    st.header("Predicted Score - " + str(int(result[0])))
