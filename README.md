# NBA-Monte-Carlo-Simulator

Welcome to my first attempt at a monte carlo simulator. This was a project that I undertook to learn more about using python for simulations. My simulation is fairly basic, but at the very least it can produce reasonable predictions. I plan to test the simulator over a period of time to see if the model can accurately predict the outcome of games.

I relied heavily on the [basketball-reference-scraper](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/README.md) package developed by Vishaal Agartha. This package scrapes Basketball-Reference.com, and saved me many hours on this project. (Thank you Vishaal!)


# Before you use the simulator

1.) Run ProbabilityFinder.py

  This script scrapes Basketball-Reference.com for the stats we will use to simulate. This script cleans the data and creates two csv files; one with all teams unadjusted Offensive Possession Probabilities and the other with unadjusted Defensive Possession Probabilities.

2.) Run Compare to Average.py
  
  Run this script to compare all the teams probabilities to the league averages. This script takes the two csv files creates form Probability Finder and compares each team's stats to the league average.  Again, this script creates two csv files used for the simulation. These csv files will are used to adjust the stats for the opponent.
  

# Running the simulation

  Currently, I have been running the simulation at the bottom of the Basketball Monte Carlo.py file, but I have hopes of making it more functional in the future.
  

#### Disclaimer: 
This model is purely for educational purposes, and I do not recommend using this model for betting or gambling purposes.
