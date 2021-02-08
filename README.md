# NBA-Monte-Carlo-Simulator

Welcome to my first attempt at a monte carlo simulator. This was a project that I undertook to learn more about using python for simulations. My simulation is fairly basic, but at the very least it can produce reasonable predictions. I plan to test the simulator over a period of time to see if the model can accurately predict the outcome of games.

This project would have much harder with out the [basketball-reference-scraper](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/README.md) package developed by Vishaal Agartha. This package scrapes Basketball-Reference.com, and saved me many hours on this project. I also use the [PySBR](https://github.com/JeMorriso/PySBR/blob/main/README.md) package developed by Jeremy Morrison to get the games for today. (Thank you Vishaal and Jeremy!)

The next step in my project is to automatically compare my predicted outcomes with betting lines to find potential value. 

# Running the simulation

  The best way to run the simulation is to use the master.py script. The script is designed to pull the games for today and run them all through the simulation. If you are interested in simulating a random game, I would recommend clearing out the main() and use one line of code -> "run_simulation(team1, team2, off_vs_avg, def_vs_avg, off_prob, 10000)".

  The other scripts are smaller chunks of the master.py script. The scripts are designed to be run individually to perform the same function as the master script. Those files were the original design of my project, but I decided to create the master script for functionality. I plan to leave the files up incase anyone would is interested in inspecting a particular part of the project. If you were to run the scripts individually, the order to run them is probability finder -> compare to average -> monte carlo.
  
My last update was to modularize my simulation code. The functions can be found in the simulation_function.py script. This is the file that the master.py script imports the run_simulation function from.   

#### Disclaimer: 
This model is purely for my own educational purposes, and I do not recommend using this model for betting or gambling purposes.
