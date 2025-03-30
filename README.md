# Bacterial-growth-model


## Run simulations and make figures 

### Figure 2
1. compile: g++ -std=c++11 -O3 simulation_figure2.cpp -o fig2_exec
2. execute: ./fig2_exec
3. plot: python plot_figure_2.py
Figure 2 is now in the main_figures folder.

### Figure 3 (Distributions of division times)
1. compile: g++ -std=c++11 -O3 simulation_figure3.cpp -o fig3_exec
2. execute: ./fig3_exec
3. plot: python plot_figure_3.py

### Figure 4 (Mean dependence on resource allocation parameters)
1. compile: g++ -std=c++11 -O3 simulation_figure4.cpp -o fig4_exec
2. execute: ./fig4_exec
3. plot: python plot_figure_4.py

### Figure 5 panel A (Occurrence of dormancy types with different growth structures)
#### Branching growth 
1. compile: g++ -std=c++11 -O3 simulation_figure5_panel_A_part1.cpp -o fig5a1_exec
2. execute: ./fig5a1_exec 
#### Lineage growth 
3. compile: g++ -std=c++11 -O3 simulation_figure5_panel_A_part2.cpp -o fig5a2_exec
4. execute: ./fig5a2_exec
#### Plot
5. plot: python plot_figure_5a.py

### Figure 5B (Cellular content during entry into dormancy state)
1. compile: g++ -std=c++11 -O3 simulation_figure5_panel_BCD.cpp -o fig5b_exec
2. execute: ./fig5b_exec
3. plot: python plot_figure_5b.py
(Generating the figure is very slow. There are most likely ways to optimize the performance.)
