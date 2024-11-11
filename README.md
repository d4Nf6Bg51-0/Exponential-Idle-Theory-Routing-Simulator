# Exponential-Idle-Theory-Routing-Simulator
Calculates a near optimal strategy to push main theories and custom theories to maximize long term gains

1) Go to ct_routing_sim.py
2) Enter your ct distribution in taus, and fill in the file addresses for ct tau lookup table and ct routing
3) Run program, it will generate near optimal way to push custom theories to maximize tau gain speed
4) Go to ct_routing.txt to see suggested path, each line is 1 publish
5) Go to main_theory_routing.py
6)  fill in the file addresses for ct tau lookup table and main theory routing txt files
7) enter students, total cts tau, main theory distribution
8) Go to ct_tau_lookup_table and scroll down to the bottom and take round down the time in days and multiply that number by 24
9) replace that number in ct_tau_gain and ct_rate
10) Go to overpush_strat_2 and set limit to t2 cap*
11) Run program, it will generate near optimal overpush and cash in cycle for you accounting for cts rates
12) See routing in main_theory_routing.txt
13) Have fun, play around with it.

*Currently the overpush advantage relative to the greedy player is between 0-4+ % time advantage. This depends highly on where you currently are and how fast your cts are. In other to catch up to the greedy player, you will eventually have to equalize all main theory rates. I highly recommend you do NOT set t2 higher than e700 to e710. 
The cash in cycle takes 7-10 years at this point. 
