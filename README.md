# Real---Time-Air-Traffic-Control-Simulation
An event-driven simulator that tracks many aircraft in 3D airspace and handles conflicts as they are predicted.
# Features
* State-machine lifecycle for each aircraft, with terminated flights pruned automatically
* Deterministic chronological ordering of events across concurrent flight trajectories
* Predicts mid-air collisions and terrain crashes by solving continuous 3D quadratic trajectory equations, handling floating-point precision
* Reroutes aircraft by computing safe alternative 3D flight vectors
