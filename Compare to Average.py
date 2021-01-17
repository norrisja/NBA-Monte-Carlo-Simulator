# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:43:01 2021

@author: norri
"""

import pandas as pd

offense = pd.read_csv('Offensive Possesion Probabilities.csv',
                      index_col = 'Teams')
defense = pd.read_csv('Defensive Possesion Probabilities.csv',
                      index_col= 'Teams')


off_avg = offense.loc['AVG']
pace = offense['Pace']
offense.drop('AVG', inplace=True)

off_vs_avg = offense - off_avg
off_vs_avg.drop('Pace', axis=1, inplace=True)


def_avg = defense.loc['AVG']
defense.drop('AVG', inplace=True)

def_vs_avg = defense - def_avg


off_vs_avg.to_csv('Offense vs Avg.csv')
def_vs_avg.to_csv('Defense vs Avg.csv')
pace.to_csv('Pace.csv')
