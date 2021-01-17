# NBA-Monte-Carlo-Simulator

Welcome to my first attempt at a monte carlo simulator. This was a project that I undertook to learn more about using python for simulations. My simulation is fairly basic, but at the very least it can produce reasonable predictions. I plan to test the simulator over a period of time to see if the model can accurately predict the outcome of games.

I used the [basketball-reference-scraper](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/README.md) package developed by Vishaal Agartha. This package scrapes Basketball-Reference.com, and saved me many hours on this project. (Thank you Vishaal)

The biggest flaw in this model is that I don't have free throws built into the model. I'm not exactly sure how to encorporate free throws into my model, but the stats necessary (FT/FTA & FT%) are readily available from the same tables I am already scraping from. Hopefully, one day I will sit down and figure out how to include free throws.


# Before you use the simulator

1.) Run ProbabilityFinder.py

  This script scrapes Basketball-Reference.com for the stats we need to simulate. This will create two csv files that we use in the other scripts.

2.) Run Compare to Average
  
  Run this script to compare all the teams probabilities to the league averages. This is used to adjust the stats for the opponent. Again, this script creates two csv files that   are used in the simulation.
  

# Running the simulation

  Currently, I have been running the simulation at the bottom of the Basketball Monte Carlo.py file, but I have hopes of making it more functional in the future.
  
