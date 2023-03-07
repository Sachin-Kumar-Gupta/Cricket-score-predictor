import streamlit as st
import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor

pl = pickle.load(open('pl.pkl','rb'))

teams = ['Mumbai Indians','Royal Challengers Bangalore','Kolkata Knight Riders',
         'Chennai Super Kings','Rajasthan Royals','Kings XI Punjab','Delhi Daredevils',
         'Sunrisers Hyderabad','Deccan Chargers','Delhi Capitals','Pune Warriors',
         'Gujarat Lions','Punjab Kings','Gujarat Titans','Rising Pune Supergiant',
         'Lucknow Super Giants','Kochi Tuskers Kerala','Rising Pune Supergiants']

venues = ["Wankhede Stadium ","Eden Gardens","M Chinnaswamy Stadium","MA Chidambaram Stadium",
         "Rajiv Gandhi International Stadium","Feroz Shah Kotla","Punjab Cricket Association IS Bindra Stadium",
         "Dubai International Cricket Stadium","Sawai Mansingh Stadium","Dr DY Patil Sports Academy",
         "Maharashtra Cricket Association Stadium","Sheikh Zayed Stadium","Sharjah Cricket Stadium",
         "Brabourne Stadium","Arun Jaitley Stadium","Subrata Roy Sahara Stadium",
         "Kingsmead","Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium","Sardar Patel Stadium",
         "SuperSport Park","Saurashtra Cricket Association Stadium","Himachal Pradesh Cricket Association Stadium",
         "Holkar Cricket Stadium","New Wanderers Stadium","Zayed Cricket Stadium",
         "Barabati Stadium","St George's Park","JSCA International Stadium Complex",
         "Narendra Modi Stadium","Newlands","Shaheed Veer Narayan Singh International Stadium",
         "Nehru Stadium","Green Park","Vidarbha Cricket Association Stadium","De Beers Diamond Oval",
         "Buffalo Park","OUTsurance Oval"]
innings = [1,2]
overs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
balls = [1,2,3,4,5,6]

st.title('Score Predictor')

col_1, col_2 = st.beta_columns(2)

with col_1:
    batting_team = st.selectbox('Select batting team',sorted(teams))
with col_2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

Venue = st.selectbox('Select city',sorted(venues))

col_3,col_4,col_5,col_6, col_7 = st.beta_columns(5)

with col_3:
    current_score = st.number_input('Current Score')
with col_4:
    overs = st.selectbox('Overs done(works for over>5)', sorted(overs))
with col_5:
    ball = st.selectbox('Ball of the over', sorted(balls))
with col_6:
    wickets = st.number_input('Wickets out')
with col_7:
    inning = st.number_input('Inning')
    
last_five = st.number_input('Runs scored in last 5 overs')

if st.button('Predict Score'):
    balls_done = (overs*6) + ball
    wickets_left = 10 -wickets
    crr = (current_score*6)/balls_done

    input_df = pd.DataFrame(
     {'Venue':Venue,'Inning':[inning],'batting_team': [batting_team], 'bowling_team': [bowling_team], 'current_score': [current_score],'wickets': [wickets],'Over': [overs],'Ball': [ball], 'crr': [crr], 'last_five': [last_five]})
    result = pl.predict(input_df)
    st.header("Predicted Score - " + str(int(result[0])))
