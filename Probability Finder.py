# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 01:13:36 2021

@author: norri
"""

import pandas as pd
from basketball_reference_scraper.teams import get_team_stats, get_opp_stats, get_team_misc

# List of NBA ref team abreviations, WAS does not work for some reason
teams = ['ATL', 'BRK', 'BOS', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'TOR', 'UTA']#, 'WAS']

df = pd.DataFrame()
for team in teams:

    team_stats = pd.DataFrame(get_team_stats(team, 2021, 'TOTAL')) 
    team_stats.columns = [team]
    df = pd.concat([df,team_stats], axis=1)
    
df2 = pd.DataFrame()

for team in teams:
    
    # This pulls two TOV% variables because they have the same name on BB ref,
    # this issue is addressed below where I create the df def_tov_df to store this variable 
    misc_stats = pd.DataFrame(get_team_misc(team, 2021)[['PACE', 'ORB%', 'TOV%', 'DRB%']])
    misc_stats.columns = [team]
    df2 = pd.concat([df2, misc_stats], axis=1)

combined_stats = pd.concat([df, df2])


def_tov_drb_df = combined_stats[-2:].copy()
def_tov_drb_df.index = ['DEF_TOV%', 'DRB%']
combined_stats = combined_stats[:-2]

data = pd.concat([combined_stats, def_tov_drb_df]).transpose()

columns = ['FGA', '3P%', '3PA', '2P%', '2PA', 'TOV%', 'ORB%', 'PACE']
data = data[columns]

data['3pt Ratio'] = data['3PA'] / data['FGA']
data['2pt Ratio'] = data['2PA'] / data['FGA']

data.drop(columns = ['3PA', '2PA', 'FGA'], inplace = True)

off_prob_df = pd.DataFrame({'3pt Ratio': [],
                            '2pt Ratio': [],
                            '3P%': [],
                            '2P%': [],
                            'ORB%': [],
                            'TOV%': [],
                            'Pace': []
                            })
 
for team in data.index:
    
    three_ratio = data.loc[team,'3pt Ratio'] 
    two_ratio = data.loc[team,'2pt Ratio']
    three = data.loc[team,'3P%'] 
    two = data.loc[team,'2P%'] 
    orb = data.loc[team,'ORB%']  
    tov = data.loc[team,'TOV%']
    pace = data.loc[team, 'PACE']
    
    off_prob_df = pd.concat([off_prob_df, pd.DataFrame({'3pt Ratio': [three_ratio],
                                                        '2pt Ratio': [two_ratio],
                                                        '3P%': [three],
                                                        '2P%': [two],
                                                        'ORB%': [orb / 100],
                                                        'TOV%': [tov / 100],
                                                        'Pace': [pace]}) 
                                                         ])
    
   
off_prob_df.index = teams
off_prob_df.loc['AVG'] = round(off_prob_df.mean(), 3)

off_prob_df.to_csv('Offensive Possesion Probabilities.csv')

### Opponent/Defensive Probabilities

# Same steps as above but for the 

opp_df = pd.DataFrame()

for team in teams:
    
    opp_stats = pd.DataFrame(get_opp_stats(team, 2021, 'TOTAL')) 
    opp_stats.columns = [team]
    
    opp_df = pd.concat([opp_df, opp_stats], axis=1)
    
df7 = pd.concat([opp_df, def_tov_drb_df])

opp_data = df7.transpose()

opp_columns = ['OPP_FGA', 'OPP_3P%', 'OPP_3PA', 'OPP_2P%', 'OPP_2PA', 'DEF_TOV%', 'DRB%']
opp_data = opp_data[opp_columns]

opp_data['3pt Ratio'] = opp_data['OPP_3PA'] / opp_data['OPP_FGA']
opp_data['2pt Ratio'] = opp_data['OPP_2PA'] / opp_data['OPP_FGA']

opp_data.drop(columns = ['OPP_3PA', 'OPP_2PA', 'OPP_FGA'], inplace = True)

def_prob_df = pd.DataFrame({'3pt Ratio': [],
                            '2pt Ratio': [],
                            '3P%': [],
                            '2P%': [],
                            'TOV%': []
                            })

for team in data.index:
    
    three_ratio = opp_data.loc[team,'3pt Ratio'] 
    two_ratio = opp_data.loc[team,'2pt Ratio']
    three = opp_data.loc[team,'OPP_3P%'] 
    two = opp_data.loc[team,'OPP_2P%'] 
    drb = opp_data.loc[team,'DRB%']  
    tov = opp_data.loc[team,'DEF_TOV%']
    
    def_prob_df = pd.concat([def_prob_df, pd.DataFrame({'3pt Ratio': [three_ratio],
                                                        '2pt Ratio': [two_ratio],
                                                        '3P%': [three],
                                                        '2P%': [two],
                                                        'aORB%': [1 - (drb / 100)], # allowed orb%
                                                        'TOV%': [tov / 100]}) 
                                                         ])
    
def_prob_df.index = teams
def_prob_df.loc['AVG'] = round(def_prob_df.mean(), 3)

def_prob_df.to_csv('Defensive Possesion Probabilities.csv')
