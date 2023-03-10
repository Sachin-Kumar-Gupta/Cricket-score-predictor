import streamlit as st
import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor
import zipfile

# specify the path of the zip file
zip_path = 'pl.zip'

# create a ZipFile object
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # extract all files to a directory
    zip_ref.extractall()

pl = pickle.load(open('pl.pkl','rb'))

venues = ['Sheikh Zayed Stadium', 'Arun Jaitley Stadium', 'Wankhede Stadium','MA Chidambaram Stadium','Himachal Pradesh Cricket Association Stadium',
         'M Chinnaswamy Stadium', 'Dubai International Cricket Stadium','Dr DY Patil Sports Academy', 'Feroz Shah Kotla',
         'Punjab Cricket Association IS Bindra Stadium','Saurashtra Cricket Association Stadium','Rajiv Gandhi International Stadium',
         'Sawai Mansingh Stadium','Kingsmead', 'Maharashtra Cricket Association Stadium','New Wanderers Stadium', 'Eden Gardens', 'SuperSport Park',
         "St George's Park", 'Subrata Roy Sahara Stadium','Sharjah Cricket Stadium', 'Vidarbha Cricket Association Stadium','Zayed Cricket Stadium',
         'Narendra Modi Stadium','Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium','Holkar Cricket Stadium', 'JSCA International Stadium Complex',
         'Sardar Patel Stadium','Shaheed Veer Narayan Singh International Stadium','Brabourne Stadium', 'De Beers Diamond Oval','OUTsurance Oval',
         'Nehru Stadium', 'Newlands', 'Barabati Stadium', 'Green Park','Buffalo Park']

teams = ['Mumbai Indians', 'Delhi Capitals', 'Chennai Super Kings','Rajasthan Royals', 'Delhi Daredevils', 'Kings XI Punjab',
         'Kolkata Knight Riders', 'Royal Challengers Bangalore','Sunrisers Hyderabad', 'Deccan Chargers', 'Pune Warriors',
         'Rising Pune Supergiants', 'Gujarat Lions', 'Kochi Tuskers Kerala','Rising Pune Supergiant']

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
