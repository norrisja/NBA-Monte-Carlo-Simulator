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

off_prob.drop(['Pace', 'FTr'], axis=1, inplace=True)


def run_simulation(team1, team2, simulations):
    
    off = np.array(off_vs_avg.drop(['FTr','Pace'], axis=1).loc[team1])
    deff = np.array(def_vs_avg.loc[team2])
    
    # Adjusted expectations for team 1 on offense
    expectations = (off + deff) + off_prob.mean()
    
    team1_tov = expectations['TOV%']
    team1_fga = 1 - expectations['TOV%']
    team1_3pa = team1_fga * expectations['3pt Ratio']
    team1_2pa = team1_fga * expectations['2pt Ratio']
    
    # A list of the probabilities of a tov, 3pa, or 2pa on any given possession
    team1_prob = [team1_tov, team1_2pa, team1_3pa]
    three = expectations['3P%']
    two = expectations['2P%']
    orb = expectations['ORB%']
    
    home_ft_rate = off_vs_avg['FTr'][team1]
    away_ft_rate = off_vs_avg['FTr'][team2]
    
    # FT rate is for both teams
    ft_rate = home_ft_rate + away_ft_rate + ftr.mean()
    
    # Calculate the proportion of fouls that happen on a 2pa vs 3pa
    ft_per_2pt_fga = ft_rate * team1_2pa
    ft_per_3pt_fga = ft_rate * team1_3pa
    
    # FT percent is just for team1
    ft_percent = expectations['FT%']
    
    game_pace = float(off_vs_avg['Pace'][team1]) + float(off_vs_avg['Pace'][team2]) + float(pace.mean())
    print(f'Estimated Game Pace: {round(game_pace)}')
          
    points = 0
    for i in range(simulations):
        
        pos_end = 0
        
        while pos_end < 1:
            
            # The probabilities is team 1's possession probabilities 
            outcome = np.random.choice(range(0,3), p=team1_prob)
            
            # The outcome is a 2pa
            if outcome == 1:
                
                # The team has a chance at being fouled every possession
                foul = np.random.choice(range(0,2), p=[1-ft_per_2pt_fga, ft_per_2pt_fga])
                
                # No foul, normal 2pt shot
                if foul == 0:
                    
                    shot_prob = np.random.rand()                
                    
                    # Shot goes in
                    if shot_prob <= two:
                        points += 2
                        pos_end = 1
                     
                    # Shot doesn't go in (ORB chance)
                    else:
                        
                        orb_prob = np.random.rand()
                        if orb_prob >= orb:
                            pos_end = 1
                    
                        # If the team gets the orb, they have a new possession
                        else: 
                            outcome = np.random.choice(range(0,3), p=team1_prob)
                
                # Fouled 2pt shot
                else:
                    shot_prob = np.random.rand()
                    
                    # Fouled and the the shot goes in
                    if shot_prob<= (two/4): # Arbitrary- getting fouled halves the chance of a shot going in 
                        
                        points += 2
                        
                        free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                        # Made free throw
                        if free_throw == 1:
                            points += 1
                            pos_end = 1
                        
                        else:
                            pos_end = 1
                    
                    # Fouled and the shot doesn't go in
                    else:
                        
                        ft_attempts = 2
                        
                        # Only run if we have ft attempts remaining
                        while ft_attempts > 0:
                       
                            free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])

                            if free_throw == 1:
                                points += 1
                                ft_attempts -= 1
                                
                                # If that was our last ft attempt, end the possession
                                if ft_attempts == 0:
                                    pos_end = 1
                                
                            else:
                                ft_attempts -= 1
                                
                                if ft_attempts == 0:
                                    pos_end = 1
                                                  
                        
            # Three point shot   
            elif outcome == 2:
                
                foul = np.random.choice(range(0,2), p=[1-ft_per_3pt_fga, ft_per_3pt_fga])
                
                 # No foul, normal 3pt shot
                if foul == 0:
                    shot_prob = np.random.rand()
                
                    if shot_prob <= three:
                        points += 3 
                        pos_end = 1
                    
                    else:
                    
                        orb_prob = np.random.rand()
                        if orb_prob >= orb:
                            pos_end = 1
                    
                        else: 
                            outcome = np.random.choice(range(0,3), p=team1_prob)
                            
                # Fouled while shooting a three            
                else:
                    
                    shot_prob = np.random.rand()
                    
                    # Fouled and the the shot goes in
                    if shot_prob <= (three/4): # Arbitrary- getting fouled halves the chance of a shot going in 
                        
                        points += 3
                        free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                        if free_throw == 1:
                            points += 1
                            pos_end = 1
                        
                        else:
                            pos_end = 1
                    
                    # Fouled and the shot doesn't go in
                    else:
                        
                        ft_attempts = 3
                        while ft_attempts > 0:
                       
                            free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                            if free_throw == 1:
                                points += 1
                                ft_attempts -= 1
                                
                                if ft_attempts == 0:
                                    pos_end = 1
                                
                            else:
                                ft_attempts -= 1 
                                    
                                if ft_attempts == 0:
                                    pos_end = 1
                            
            # TOV            
            else: 
                
                pos_end = 1
                
                

     
    points_per_poss =  points / simulations
    
    print(f'{team1} averaged {points_per_poss} points per possession')
    
    
    off2 = np.array(off_vs_avg.drop(['FTr', 'Pace'], axis=1).loc[team2])
    deff2 = np.array(def_vs_avg.loc[team1])
    
    expectations2 = (off2 + deff2) + off_prob.mean()
    
    team2_tov = expectations2['TOV%']
    team2_fga = 1 - expectations2['TOV%']
    team2_3pa = team2_fga * expectations2['3pt Ratio']
    team2_2pa = team2_fga * expectations2['2pt Ratio']
    
    team2_prob = [team2_tov, team2_2pa, team2_3pa]
    three2 = expectations2['3P%']
    two2 = expectations2['2P%']
    orb2 = expectations2['ORB%']
        
    ft_per_2pt_fga = ft_rate * team2_2pa
    ft_per_3pt_fga = ft_rate * team2_3pa
    
    ft_percent = expectations2['FT%']
        
    team2_points = 0
    for i in range(simulations):
        
        pos_end = 0
        
        while pos_end < 1:
            outcome = np.random.choice(range(0,3), p=team2_prob)
            
            if outcome == 1:
                
                foul = np.random.choice(range(0,2), p=[1-ft_per_2pt_fga, ft_per_2pt_fga])
                
                 # No foul, normal 2pt shot
                if foul == 0:
                    
                    shot_prob = np.random.rand()                
                    
                     # Shot goes in
                    if shot_prob <= two2:
                        team2_points += 2
                        pos_end = 1
                     
                    # Shot doesn't go in (ORB chance)
                    else:
                        
                        orb_prob = np.random.rand()
                        if orb_prob >= orb2:
                            pos_end = 1
                    
                        else: 
                            outcome = np.random.choice(range(0,3), p=team2_prob)
                
                # Fouled 2pt shot
                else:
                    shot_prob = np.random.rand()
                    
                    # Fouled and the the shot goes in
                    if shot_prob <= (two2/4): # Arbitrary- getting fouled halves the chance of a shot going in 
                        
                        team2_points += 2
                        
                        free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                        if free_throw == 1:
                            team2_points += 1
                            pos_end = 1
                        
                        else:
                            pos_end = 1
                    
                    # Fouled and the shot doesn't go in
                    else:
                        
                        ft_attempts = 2
                        while ft_attempts > 0:
                       
                            free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                            if free_throw == 1:
                                team2_points += 1
                                ft_attempts -= 1
                                
                                if ft_attempts == 0:
                                    pos_end = 1
                                
                            else:
                                ft_attempts -= 1
                                
                                if ft_attempts == 0:
                                    pos_end = 1
                
                                                   
                        
            # Three point shot   
            elif outcome == 2:
                
                foul = np.random.choice(range(0,2), p=[1-ft_per_3pt_fga, ft_per_3pt_fga])
                
                 # No foul, normal 3pt shot
                if foul == 0:
                    shot_prob = np.random.rand()
                
                    if shot_prob <= three2:
                        team2_points += 3 
                        pos_end = 1
                    
                    else:
                    
                        orb_prob = np.random.rand()
                        if orb_prob >= orb2:
                            pos_end = 1
                    
                        else: 
                            outcome = np.random.choice(range(0,3), p=team2_prob)
                            
                # Fouled while shooting a three            
                else:
                    
                    shot_prob = np.random.rand()
                    
                    # Fouled and the the shot goes in
                    if shot_prob <= (three2/4): # Arbitrary- getting fouled halves the chance of a shot going in 
                        
                        team2_points += 3
                        free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                        if free_throw == 1:
                            team2_points += 1
                            pos_end = 1
                        
                        else:
                            pos_end = 1
                    
                    # Fouled and the shot doesn't go in
                    else:
                        
                        ft_attempts = 3
                        while ft_attempts > 0:
                       
                            free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
                            
                            if free_throw == 1:
                                team2_points += 1
                                ft_attempts -= 1
                                
                                if ft_attempts == 0:
                                    pos_end = 1
                                
                            else:
                                ft_attempts -= 1 
                                    
                                if ft_attempts == 0:
                                    pos_end = 1
                            
            # TOV            
            else: 
                
                pos_end = 1            
    
  
    points_per_poss2 =  team2_points / simulations
    print(f'{team2} averaged {points_per_poss2} points per possession')
    
    print(f'{team1}: {points_per_poss * game_pace} | {team2}: {points_per_poss2 * game_pace}')
    print('_____________________________________________________')

    return_df = pd.DataFrame({f'{team1}': [round(points_per_poss * game_pace,0)],
                              f'{team2}': [round(points_per_poss2 * game_pace,0)]})    
    
    return_df = return_df.transpose()
    return_df.columns = ['Points']
    
    return return_df


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
    
    games = [(teams.get(team[0], team[0]), teams.get(team[1], team[1])) for team in games]
        
    
    predictions = pd.DataFrame()
    
    count = 0
    for game in games:
        team1 = game[0]
        team2 = game[1]
        
        df = run_simulation(team1, team2, 10000)
        
        predictions = pd.concat([predictions, df])

    predictions.to_csv("Today's Predictions.csv")    
    

