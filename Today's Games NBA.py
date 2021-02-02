# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 10:13:00 2021

@author: norri
"""

import pandas as pd
from pysbr import * 
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
today = datetime.strptime(today, '%Y-%m-%d')


# Get today's games
nba = NBA()
e = EventsByDate(nba.league_id, today)

cols = ['event id', 'event status',
        'participants.1.source.abbreviation', 'participants.1.participant id',
        'participants.2.source.abbreviation', 'participants.2.participant id']

games_today = e.dataframe()[cols]
games_today

games = []

for i in range(len(games_today)):
    games.append((games_today['participants.1.source.abbreviation'][i], games_today['participants.2.source.abbreviation'][i]))
    
    
teams = {'ATL':'ATL', 'BKN': 'BRK', 'BOS': 'BOS', 'CHA': 'CHO', 'CHI': 'CHI', 
         'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN', 'DET': 'DET', 'GSW': 'GSW',
         'HOU': 'HOU', 'IND': 'IND', 'LAC': 'LAC', 'LAL': 'LAL', 'MEM': 'MEM',
         'MIA': 'MIA', 'MIL': 'MIL', 'MIN': 'MIN', 'NOP': 'NOP', 'NYK': 'NYK',
         'OKC': 'OKC', 'ORL': 'ORL', 'PHI': 'PHI', 'PHX': 'PHO', 'POR': 'POR',
         'SAC': 'SAC', 'SAS': 'SAS', 'TOR': 'TOR', 'UTA': 'UTA', 'WAS': 'WAS'}

games = [(teams.get(team[0], team[0]), teams.get(team[1], team[1])) for team in games]