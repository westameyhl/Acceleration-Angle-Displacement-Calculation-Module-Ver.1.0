Editor: WestameYHL
Update Time: 2025/05/27

Program Structure
=====================================
Main Execution File: mainfunc_xxxx.py
A. Basic program framework for a single computation
B. for p in i_power: Vary the power to calculate the loss under different power values
C. for dp in i_dp_list1: Vary the breakpoint location to compute power and assess whether the breakpoint can be detected
D. Change the magnitude of external force to observe if the fitting results vary

Includes a decorator for efficiency monitoring, used to plan computation sequences and output endpoints.

Four Core Modules ("Kings")
PMK:Instantiates the model and acts as the core object of the entire computation. It stores various physical and mathematical parameters for each segment and determines the rules and precision for each element's computation.
Generator:Uses the PMK object to generate the KKT matrix and perform mathematical solving.
Objects:Defines basic computational elements (nodes, slices, point pairs, connections).
INP:Input interface for adding constraints, connections, etc., enabling modular model assembly.

Toolkits (tools)
loss_func:Interface for damage/loss computation; supports multiple damage calculation rules.
EarthMovingCalculator: Code for computing EMD (Earth Mover's Distance)
LocalPlot:Plotting output interface, compatible with various custom plotting functions.
LoggingPMK:Logging output interface; outputs command-line logs to .txt files.
DataLoader:Loads data from files into variables (supports .mat, .csv, .txt).
ParticalTopo:Topological damage modeling.
FxZeros:A bisection-method framework for zero-point calculation, useful for Tikhonov regularization terms.

Configuration Files (settings)
config.txt: Stores basic model parameters and data input locations
input_data2pxy.py: Plugin for manually calculating p_xy subroutines
plot_setting.py: Plugin for configuring plot parameters
custom_power.py: Plugin for manually setting model parameters for each computational unit

Raw Dataset (data)
Contains various data files


