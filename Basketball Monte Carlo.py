# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:38:46 2021

@author: norri
"""
import pandas as pd
import numpy as np

off_prob = pd.read_csv('Offensive Possession Probabilities.csv',
                       index_col='Teams')

def_prob = pd.read_csv('Defensive Possession Probabilities.csv',
                       index_col='Teams')

off_vs_avg = pd.read_csv('Offense vs Avg.csv',
                         index_col='Teams')

def_vs_avg = pd.read_csv('Defense vs Avg.csv',
                         index_col='Teams')

pace = off_prob['Pace']
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
                    if shot_prob<= (two/4): # The best research I could find was that in '05-'06, the league averaged 28.2 FG% on shooting fouls --> http://www.82games.com/andone.htm
                        
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
                    if shot_prob <= (three/4): 
                        
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
    
    
    off2 = np.array(off_vs_avg.drop(['FTr','Pace'], axis=1).loc[team2])
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
                    if shot_prob <= (two2/4):
                        
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
                    if shot_prob <= (three2/4): 
                        
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


if __name__== '__main__':
    run_simulation('BOS','LAL', 10000)
    
