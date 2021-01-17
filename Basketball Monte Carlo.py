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

off_prob.drop('Pace', axis=1, inplace=True)


def run_simulation(team1, team2, simulations):
    
    off = np.array(off_vs_avg.loc[team1])
    deff = np.array(def_vs_avg.loc[team2])
    
    expectations = (off + deff) + off_prob.mean()
    
    team1_tov = expectations['TOV%']
    team1_fga = 1 - expectations['TOV%']
    team1_3pa = team1_fga * expectations['3pt Ratio']
    team1_2pa = team1_fga * expectations['2pt Ratio']
    
    team1_prob = [team1_tov, team1_3pa, team1_2pa]
    three = expectations['3P%']
    two = expectations['2P%']
    orb = expectations['ORB%']
    
    points = 0
    for i in range(simulations):
        
        pos_end = 0
        
        while pos_end < 1:
            outcome = np.random.choice(range(0,3), p=team1_prob)
            
            if outcome == 1:
                shot_prob = np.random.rand()                
            
                if shot_prob <= two:
                        points += 2
                        pos_end = 1
                    
                else:
                        
                    orb_prob = np.random.rand()
                    if orb_prob >= orb:
                        pos_end = 1
                    
                    else: 
                        outcome = np.random.choice(range(0,3), p=team1_prob)
                    
            elif outcome == 2:
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
                        
            else: 
                
                pos_end = 1
     
    points_per_poss =  points / simulations
    print(f'{team1} averages {points_per_poss} points per possession')
    
    
    off2 = np.array(off_vs_avg.loc[team2])
    deff2 = np.array(def_vs_avg.loc[team1])
    
    expectations2 = (off2 + deff2) + off_prob.mean()
    
    team2_tov = expectations2['TOV%']
    team2_fga = 1 - expectations2['TOV%']
    team2_3pa = team2_fga * expectations2['3pt Ratio']
    team2_2pa = team2_fga * expectations2['2pt Ratio']
    
    team2_prob = [team2_tov, team2_3pa, team2_2pa]
    three2 = expectations2['3P%']
    two2 = expectations2['2P%']
    orb2 = expectations2['ORB%']
    
    team2_points = 0
    for i in range(simulations):
        
        pos_end = 0
        
        while pos_end < 1:
            outcome = np.random.choice(range(0,3), p=team2_prob)
            
            if outcome == 1:
                shot_prob = np.random.rand()                
            
                if shot_prob <= two2:
                        team2_points += 2
                        pos_end = 1
                    
                else:
                        
                    orb_prob = np.random.rand()
                    if orb_prob >= orb2:
                        pos_end = 1
                    
                    else: 
                        outcome = np.random.choice(range(0,3), p=team2_prob)
                    
            elif outcome == 2:
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
                        
            else: 
                
                pos_end = 1
     
    points_per_poss2 =  team2_points / simulations
    print(f'{team2} averages {points_per_poss2} points per possession')
    
    
    return f'{team1}: {points_per_poss * pace[team1]}, {team2}: {points_per_poss2 * pace[team2]}'

