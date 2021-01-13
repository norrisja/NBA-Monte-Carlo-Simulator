# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:38:46 2021

@author: norri
"""

import numpy as np
import pandas as pd

# Simulate a basketball possesion
possesions = 10000

# Outcomes of a possesion- 2p, 3p, TO, orb, drb, ... Ignore FT for now
# These numbers are league averages as of 1/13/2021
prob = [.278, .127, .148, .096, .351]

points = 0 
for i in range(possesions):
    
    # Choose a random outcome
    outcome = np.random.choice(range(0,5), p=prob)
    
    # If the outcome is an ORB, choose a new outcome for the possesion
    while outcome == 3:
        outcome = np.random.choice(range(0,5), p=prob)
        
    # If the outcome is a TO or DRB, then continue
    if outcome == 2 or outcome == 4:
        continue
    
    if outcome == 0:
        points += 2
        
    if outcome == 1:
        points += 3

print(points/possesions)  
print(points/possesions * 100.6)
