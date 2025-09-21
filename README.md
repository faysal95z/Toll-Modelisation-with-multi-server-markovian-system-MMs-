```
# Toll Plaza Queueing Simulation (M/M/s Model)

A Python simulation of a highway toll plaza using a Multi-Server Markovian System (M/M/s queue). Models vehicle arrivals and service times across different payment types (telepayment, card, cash) to analyze queue dynamics and optimize booth allocation.

## Features
- Simulates Poisson arrival process and exponential service times
- Configurable number of booths per payment type
- Visualizes queue states and average vehicle flow
- Analyzes system performance to reduce waiting times

## Requirements
- Python 3.x
- numpy
- matplotlib

## Usage
1. Run `script.py`
2. Follow prompts to input simulation parameters
3. View generated plots of queue states and average traffic

## Parameters
- Duration (minutes)
- Number of booths per payment type
- Vehicle proportions per payment method
- Arrival rate (vehicles/minute)
- Service times per payment type

The simulation outputs graphical representations of queue states and a plot of average vehicles per booth over time.
```
