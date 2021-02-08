# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 07:26:13 2021

@author: norri
"""

import numpy as np
import pandas as pd
from datetime import datetime
from basketball_reference_scraper.teams import get_team_stats, get_opp_stats, get_team_misc
from pysbr import NBA, EventsByDate
from simulation_functions import run_simulation

# List of NBA ref team abreviations
teams = ['ATL', 'BRK', 'BOS', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

df = pd.DataFrame()
for team in teams:

    team_stats = pd.DataFrame(get_team_stats(team, 2021, 'TOTAL')) 
    team_stats.columns = [team]
    df = pd.concat([df,team_stats], axis=1)
    
df2 = pd.DataFrame()

for team in teams:
    
    # This pulls two TOV% variables because they have the same name on BB ref,
    # this issue is addressed below where I create the df def_tov_df to store this variable 
    misc_stats = pd.DataFrame(get_team_misc(team, 2021)[['PACE', 'FTr', 'ORB%', 'TOV%', 'DRB%']])
    misc_stats.columns = [team]
    df2 = pd.concat([df2, misc_stats], axis=1)

combined_stats = pd.concat([df, df2])

# Seperate the two defensive stats into a different dataframe
def_tov_drb_df = combined_stats[-2:].copy()
def_tov_drb_df.index = ['DEF_TOV%', 'DRB%']
combined_stats = combined_stats[:-2]

data = pd.concat([combined_stats, def_tov_drb_df]).transpose()

columns = ['FGA', '3P%', '3PA', '2P%', '2PA', 'FT%', 'TOV%', 'ORB%', 'PACE', 'FTr']
data = data[columns]

data['3pt Ratio'] = data['3PA'] / data['FGA']
data['2pt Ratio'] = data['2PA'] / data['FGA']

data.drop(columns = ['3PA', '2PA', 'FGA'], inplace = True)

off_prob_df = pd.DataFrame({'3pt Ratio': [],
                            '2pt Ratio': [],
                            '3P%': [],
                            '2P%': [],
                            'ORB%': [],
                            'FT%': [],
                            'TOV%': [],
                            'Pace': [],
                            'FTr': []
                            })
 
for team in data.index:
    
    three_ratio = data.loc[team,'3pt Ratio'] 
    two_ratio = data.loc[team,'2pt Ratio']
    three = data.loc[team,'3P%'] 
    two = data.loc[team,'2P%'] 
    orb = data.loc[team,'ORB%']  
    ft_percent = data.loc[team, 'FT%']
    tov = data.loc[team,'TOV%']
    pace = data.loc[team, 'PACE']
    ftr = data.loc[team, 'FTr']
    
    off_prob_df = pd.concat([off_prob_df, pd.DataFrame({'3pt Ratio': [three_ratio],
                                                        '2pt Ratio': [two_ratio],
                                                        '3P%': [three],
                                                        '2P%': [two],
                                                        'ORB%': [orb / 100],
                                                        'FT%': [ft_percent],
                                                        'TOV%': [tov / 100],
                                                        'Pace': [pace],
                                                        'FTr': [ftr]}) 
                                                         ])
    
   
off_prob_df.index = teams
off_prob_df.index.name = 'Teams'
off_prob_df.loc['AVG'] = round(off_prob_df.mean(), 3)

### Opponent/Defensive Probabilities

# Same steps as above but for the opponent stats

opp_df = pd.DataFrame()

for team in teams:
    
    opp_stats = pd.DataFrame(get_opp_stats(team, 2021, 'TOTAL')) 
    opp_stats.columns = [team]
    
    opp_df = pd.concat([opp_df, opp_stats], axis=1)
    
df7 = pd.concat([opp_df, def_tov_drb_df])

opp_data = df7.transpose()

opp_columns = ['OPP_FGA', 'OPP_3P%', 'OPP_3PA', 'OPP_2P%', 'OPP_2PA', 'DEF_TOV%', 'OPP_FT%', 'DRB%']
opp_data = opp_data[opp_columns]

opp_data['3pt Ratio'] = opp_data['OPP_3PA'] / opp_data['OPP_FGA']
opp_data['2pt Ratio'] = opp_data['OPP_2PA'] / opp_data['OPP_FGA']

opp_data.drop(columns = ['OPP_3PA', 'OPP_2PA', 'OPP_FGA'], inplace = True)

def_prob_df = pd.DataFrame({'3pt Ratio': [],
                            '2pt Ratio': [],
                            '3P%': [],
                            '2P%': [],
                            'TOV%': [],
                            'FT%': [],
                            })

for team in data.index:
    
    three_ratio = opp_data.loc[team,'3pt Ratio'] 
    two_ratio = opp_data.loc[team,'2pt Ratio']
    three = opp_data.loc[team,'OPP_3P%'] 
    two = opp_data.loc[team,'OPP_2P%'] 
    drb = opp_data.loc[team,'DRB%']  
    tov = opp_data.loc[team,'DEF_TOV%']
    ft_percent = opp_data.loc[team, 'OPP_FT%']
    
    def_prob_df = pd.concat([def_prob_df, pd.DataFrame({'3pt Ratio': [three_ratio],
                                                        '2pt Ratio': [two_ratio],
                                                        '3P%': [three],
                                                        '2P%': [two],
                                                        'aORB%': [1 - (drb / 100)], # allowed orb%
                                                        'TOV%': [tov / 100],
                                                        'FT%': [ft_percent]}) 
                                                         ])
    
def_prob_df.index = teams
def_prob_df.index.name = 'Teams'
def_prob_df.loc['AVG'] = round(def_prob_df.mean(), 3)

# Compare the probabilities to the average

offense = off_prob_df
defense = def_prob_df

off_avg = offense.loc['AVG']
offense.drop('AVG', inplace=True)

off_vs_avg = offense - off_avg

def_avg = defense.loc['AVG']
defense.drop('AVG', inplace=True)

def_vs_avg = defense - def_avg


# Run the simulation
off_prob = off_prob_df
def_prob = def_prob_df

pace = pd.DataFrame(off_prob['Pace'])

ftr = off_prob['FTr']


#off_prob.drop(['Pace', 'FTr'], axis=1, inplace=True)


if __name__== '__main__':
    
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
    
    # Attempt to find a replacement, in the dictionary, else leave the current value
    games = [(teams.get(team[0], team[0]), teams.get(team[1], team[1])) for team in games]
        
    
    predictions = pd.DataFrame()
    
    count = 0
    for game in games:
        team1 = game[0]
        team2 = game[1]
        
        df = run_simulation(team1, team2, off_vs_avg, def_vs_avg, off_prob, 10000)
        
        predictions = pd.concat([predictions, df])

    predictions.to_csv("Today's Predictions.csv")
