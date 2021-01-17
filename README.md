# NBA-Monte-Carlo-Simulator

Welcome to my first attempt at a monte carlo simulator. This was a project that I undertook to learn more about using python for simulations. My simulation is fairly basic, but at the very least it can produce reasonable predictions. I plan to test the simulator over a period of time to see if the model can accurately predict the outcome of games.

I used the [basketball-reference-scraper](https://github.com/vishaalagartha/basketball_reference_scraper/blob/master/README.md) package developed by Vishaal Agartha. This package scrapes Basketball-Reference.com, and saved me many hours on this project. (Thank you Vishaal)

The biggest flaw in this model is that I don't have free throws built into the model. I'm not exactly sure how to encorporate free throws into my model, but the stats necessary (FT/FTA & FT%) are readily available from the same tables I am already scraping from. Hopefully, one day I will sit down and figure out how to include free throws.


# How to use the simulator

1.) Run ProbabilityFinder.py
