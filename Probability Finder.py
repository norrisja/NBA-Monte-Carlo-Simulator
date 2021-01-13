# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 01:13:36 2021

@author: norri
"""

from basketball_reference_scraper.teams import get_team_stats

# Fill in with list of NBA ref team abreviations
teams = ['ATL', 'BRK', 'BOS', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
         'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
         'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'TOR', 'UTA']#, 'WAS	']

df = pd.DataFrame()
for team in teams:
    
    print(team)
    df2 = pd.DataFrame(get_team_stats(team, 2021, 'TOTAL'))
    
    df = pd.concat([df,df2], axis=1)
    
df.columns = df.loc['TEAM']
    
    

#%%
data = df.transpose()

columns = ['3P', '2P', 'ORB', 'DRB', 'TOV']
data = data[columns]
data['Total'] = data['3P'] + data['2P'] + data['ORB'] + data['DRB'] + data['TOV']


prob_df = pd.DataFrame({'3P': [],
                        '2P': [],
                        'ORB': [],
                        'DRB': [],
                        'TOV': []
                        })

for team in data.index:
    three = data.loc[team,'3P'] / data.loc[team, 'Total']
    two = data.loc[team,'2P'] / data.loc[team, 'Total']
    orb = data.loc[team,'ORB'] / data.loc[team, 'Total']
    drb = data.loc[team,'DRB'] / data.loc[team, 'Total']
    tov = data.loc[team,'TOV'] / data.loc[team, 'Total']
    
    prob_df = pd.concat([prob_df, pd.DataFrame({'3P': [three],
                                                '2P': [two],
                                                'ORB': [orb],
                                                'DRB': [drb],
                                                'TOV': [tov]
                                                }) 
                                                 ])
