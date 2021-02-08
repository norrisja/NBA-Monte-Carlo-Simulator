def foul(ft_per_Xpt_fga):
    """ Determines if there was a foul on a given possession.
    
    No Foul = 0
    Foul = 1
    """
    
    foul = np.random.choice(range(0,2), p=[1-ft_per_Xpt_fga, ft_per_Xpt_fga])
    
    return foul

def ft_attempt(ft_percent, num_fts):
    """ Simulates a ft attempt\s given a ft percentage and number of attempts""" 
    
    count = 0
    points = 0
    while count != num_fts:
        
        free_throw = np.random.choice(range(0,2), p=[1-ft_percent, ft_percent])
        
        # Made free throw
        if free_throw == 1:
            points += 1
            count += 1    
            
        else:
            count += 1
    
    return points

def offensive_rebound(orb_prob):
    """ Simulates the chances of a team getting an offensive rebound.
    
    returns True for an offensive rebound
    returns False for a defensive rebound
    """
    
    orb_chance = np.random.rand()
    
    # Yes, there was an offensive rebound
    if orb_chance <= orb_prob:
        return True
    
    else:
        return False

def two_point_attempt(two_point_make_percent, ft_per_2pt_fga, ft_percent, orb_prob):
    """ Simulates a two point shot attempt. 
    
    Inputs:
        two point make percentage
        the rate that the team attempts a ft per 2pa taken
        the team's ft_percent
        the team's orb%.
    
    Output is 
        0-3 for points scored
        True for an offensive rebound
        False for a defensive rebound
    """
    
    fouled = foul(ft_per_2pt_fga)
    shot_prob = np.random.rand() 
    
    # If there was no foul
    if fouled == 0:
           
        # Shot goes in
        if shot_prob <= two_point_make_percent:
            
            return 2
         
        # Shot doesn't go in (ORB chance)
        else:
            
            # returns True for an orb and False for a drb
            orb = offensive_rebound(orb_prob)
            
            return orb
                
    # There was a foul                   
    else:
                    
        # Fouled and the the shot goes in 
        if shot_prob <= (two_point_make_percent/4):
            
            
            return 2 + ft_attempt(ft_percent, 1)
                        
        # Fouled and the shot doesn't go in
        else:
            
            return ft_attempt(ft_percent, 2)
                
def three_point_attempt(three_point_make_percent, ft_per_3pt_fga, ft_percent, orb_prob):
    """ Simulates a three point shot attempt. 
    
    Inputs:
        three point make percentage
        the rate that the team attempts a ft per 3pa taken
        the team's ft_percent
        the team's orb%.
    
    Output is 
        0-4 for points scored
        True for an offensive rebound
        False for a defensive rebound
    """
    
    fouled = foul(ft_per_3pt_fga)
    shot_prob = np.random.rand() 
    
    # If there was no foul
    if fouled == 0:
           
        # Shot goes in
        if shot_prob <= three_point_make_percent:
            
            return 3
         
        # Shot doesn't go in (ORB chance)
        else:
            
            # returns True for an orb and False for a drb
            orb = offensive_rebound(orb_prob)
            
            return orb
                
    # There was a foul                   
    else:
                    
        # Fouled and the the shot goes in 
        if shot_prob <= (three_point_make_percent/4):
  
            return 3 + ft_attempt(ft_percent, 1)
                        
        # Fouled and the shot doesn't go in
        else:
            
            return ft_attempt(ft_percent, 3)  

def simulate_possession(poss_prob, shot_prob, ft_prob, ft_percent, orb_percent):
    """ Simulates one possesion of offense. 
    
        Team Probabilites should be in the order of ['TOV prob', '2PA prob', '3PA prob']
        Shot Probabilities should be in the order of ['2pt fg%, '3pt fg%]
        Free Throw Probabilities should be in the order ['ft_per_2pt_fga', 'ft_per_3pt_fga']
        FT Percent is the team's free throw percentage
        ORB Percent is the teams offensive rebound percentage
        """

    two_make_percent = shot_prob[0]
    three_make_percent = shot_prob[1]
    
    ft_per_2pt_fga = ft_prob[0]
    ft_per_3pt_fga = ft_prob[1]
    
    points = 0
    
    # Default that offense has rebound. Loop breaks when defense gets rebound.
    rebound = True
    
    # Rebound will be changed to false if they allow a defensive rebound
    while rebound == True:
        
        # The probabilities is team 1's possession probabilities 
        outcome = np.random.choice(range(0,3), p=poss_prob)
         
        # Two point shot                     
        if outcome == 1:
        
            result = two_point_attempt(two_make_percent, ft_per_2pt_fga, ft_percent, orb_percent)
            
            # Missed shot and no rebound
            if result == False:
                rebound = False
                
            # Missed shot but rebound
            elif result == True:
                rebound = True
        
            # Score
            else:
                points += result
                rebound = False
    
        # Three point shot       
        elif outcome == 2: 
            
            result = three_point_attempt(three_make_percent, ft_per_3pt_fga, ft_percent, orb_percent)
            
            # Missed Shot No Rebound
            if result == False:
                rebound = False
                
            # Misses Shot, Rebound
            elif result == True:
                rebound = True
        
            # Made Shot
            else:
                points += result
                rebound = False
            
        # TOV
        else:
            
            # Setting the rebound to false will end the possession
            rebound = False
    
    # Returns the points scored on that simulated possession
    return points   

def run_simulation(team1, team2, simulations):
    
    # First, gather the right data to simulate team1 on offense
    off = np.array(off_vs_avg.drop(['FTr','Pace'], axis=1).loc[team1])
    deff = np.array(def_vs_avg.loc[team2])
    
    # Adjusted expectations for team 1 on offense
    expectations = (off + deff) + off_prob.mean()
    
    # Extract the items in the expectations list to be variables    
    team1_tov = expectations['TOV%']
    team1_fga = 1 - expectations['TOV%']
    team1_3pa = team1_fga * expectations['3pt Ratio']
    team1_2pa = team1_fga * expectations['2pt Ratio']
    
    # A list of the probabilities of a tov, 2pm, or 3pm on any given possession
    team1_poss_prob = [team1_tov, team1_2pa, team1_3pa]
    three = expectations['3P%']
    two = expectations['2P%']
    orb = expectations['ORB%']
    
    team1_shot_prob = [two, three]
               
    home_ft_rate = off_vs_avg['FTr'][team1]
    away_ft_rate = off_vs_avg['FTr'][team2]
    
    # FT rate is for both teams
    ft_rate = home_ft_rate + away_ft_rate + ftr.mean()
    
    # Calculate the proportion of fouls that happen on a 2pa vs 3pa
    ft_per_2pt_fga = ft_rate * team1_2pa
    ft_per_3pt_fga = ft_rate * team1_3pa
    
    team1_ft_prob = [ft_per_2pt_fga, ft_per_3pt_fga]
    
    # FT percent is just for team1
    ft_percent = expectations['FT%']
    
    game_pace = float(off_vs_avg['Pace'][team1]) + float(off_vs_avg['Pace'][team2]) + float(pace.mean())
    print(f'Estimated Game Pace: {round(game_pace,1)}')
    
    points = 0
    
    for i in range(simulations):

        points += simulate_possession(team1_poss_prob, team1_shot_prob, team1_ft_prob, ft_percent, orb)
 
    points_per_poss =  points / simulations
    
    print(f'{team1} averages {points_per_poss} points per possession')
    
    # Now we get the data to simulate team 2 on offense
    off2 = np.array(off_vs_avg.drop(['FTr', 'Pace'], axis=1).loc[team2])
    deff2 = np.array(def_vs_avg.loc[team1])
    
    expectations2 = (off2 + deff2) + off_prob.mean()
    
    team2_tov = expectations2['TOV%']
    team2_fga = 1 - expectations2['TOV%']
    team2_3pa = team2_fga * expectations2['3pt Ratio']
    team2_2pa = team2_fga * expectations2['2pt Ratio']
    
    team2_poss_prob = [team2_tov, team2_2pa, team2_3pa]
    three2 = expectations2['3P%']
    two2 = expectations2['2P%']
    orb2 = expectations2['ORB%']
    
    team2_shot_prob = [two2, three2]
        
    # FT percent is just for team2
    ft_percent = expectations2['FT%']
        
    home_ft_rate = off_vs_avg['FTr'][team1]
    away_ft_rate = off_vs_avg['FTr'][team2]
    
    # Calculate the proportion of fouls that happen on a 2pa vs 3pa
    ft_per_2pt_fga = ft_rate * team2_2pa #Using the ft_rate calculated in line 247
    ft_per_3pt_fga = ft_rate * team2_3pa
    
    team2_ft_prob = [ft_per_2pt_fga, ft_per_3pt_fga]    
        
    team2_points = 0
    for i in range(simulations):
        
        team2_points += simulate_possession(team2_poss_prob, team2_shot_prob, team2_ft_prob, ft_percent, orb2)
    
  
    points_per_poss2 =  team2_points / simulations
    print(f'{team2} averaged {points_per_poss2} points per possession')
    
    print(f'{team1}: {round(points_per_poss * game_pace, 1)} | {team2}: {round(points_per_poss2 * game_pace, 1)}')
    print(f'Proj. O/U: +/- {round((points_per_poss * game_pace) + (points_per_poss2 * game_pace),1)}')
    print('_____________________________________________________')

    return_df = pd.DataFrame({f'{team1}': [round(points_per_poss * game_pace,0)],
                              f'{team2}': [round(points_per_poss2 * game_pace,0)]})    
    
    return_df = return_df.transpose()
    return_df.columns = ['Points']
    
    return return_df
