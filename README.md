# Projects
There are 2 directories: Academic and Side Projects

## Academic
Includes projects that were part of my PhD research
### Location_Lacey.m
One of the methods I used for quantifying mixing in particles
from our simulations. This method was presented in Bergantz et
al., 2015, Nature Geosciences, to demonstrate how particles mix
in a fluidized magma reservoir. We found a linear correlation
between mixing and scaled velocity, demonstrating the
establishment  of a self-similar regime of mixing. [MATLAB]
### Nearest_Neighbor.m
An improved method of quantifying particle mixing that is
sample-size independent. This method was presented in Schleicher
et al., 2016, Geophysical Research Letters and showed that
particle dispersion increases with time and can be fit with an
exponential curve. We used this exponential relationship to
extrapolate the results of our simulations to real magmatic
conditions and estimated mixing timescales to be on the order of
days, the same time-frame as that estimated from geochemical
studies. [MATLAB]
### Calculating_crystal_reactions.ipynb
An interactive Jupyter Notebook that allows users to explore how particles (crystals)
interacting with new magma will grow or dissolve. This interaction includes a
time-series forecasting calculation of exponential smoothing to account for the
"memory" a crystal has of previous magmas it has interacted with. This code was
presented at the ENKI workshop, and has been used by over 40 researchers. [PYTHON]

## Side Projects
Projects I've done for fun to practice learning python and pandas as well as
image processing and web scraping.
### movie_database.py
A short project that examined the domestic box office records would change if
inflation were accounted for. I scraped www.the-numbers.com/box-office-records/ to
get the top 5000 grossing movies, then calculated inflation rates from CPI records in
the US, as well as average ticket prices. [PYTHON}
### bead_patterns.py
A start to a project that would pixelate an input image so it could be used as
a beading pattern. [PYTHON]
