import math

sigma =  361 #enter your current students, however it will recalculate this to a higher number if you are underpushed
time = 0

#main_theory_values = [668,710,671.3,853.2,1000.2,1424.6,625.7,537.4] # t1,t2,t3,t4,t5,t6,t7,t8
main_theory_values = [601, 611, 580, 673, 858, 1027, 542, 500]
#main_theory_values = [487,484,472,619,757,880,473,423]
# 558 475 557 636 839 895 529 473
#main_theory_values = [243,295,221,232,361,194,227,277]


cts = 2062 # enter current total cts tau


main_theory_rates = [0, 0, 0, 0, 0, 0, 0, 0,]

tau_start = sum(main_theory_values) + cts
tau_current = tau_start + cts

#used to approximiate tau/hr of main theories, assumes constant pub length, data taken from xlii sim

decay = [29.8937, 37.4977, 31.8269, 45.0338, 39.9665, 103.3086, 28.1129, 17.6653]
pub_length = [2.667, 19.553, 2.705, 3.706, 2.831, 6.47, 2.667, 2.7]

scaled = [0.000304, 0.4556, 0.0002976, 0.00435, 0.000275, 0.056, 0.00029, 0.00029]
scaled_values = [544, 423, 552, 594, 832, 791, 519, 467]



"""def ct_tau_gain(cts,time):
    #return 1869
    if (((time-0)/24)*1000) < len(ct_data):  #go to the end of ct_data rounded down to nearest time in days and multiply by 24 replace this number here so it doesnt go out of range
        cts = ct_data[round((time-0)/24*1000)]
        #if(time < 26736):
            #cts = cts/4
    else:
        cts = 3600
    return cts

def ct_rate(time):
    avg = 30 # calculates tau/hr of cts over an average of x days, changing this values will not affect results much
    #if time < 7368:
    #    return 0.03
    #elif time < 26736:
    #    return (((ct_data[round(((time-7368)/24+avg)*1000)+1]-ct_data[round((time-7368)/24*1000)])*1000/24)/(1000*avg))/1
    #elif time < (76944-24*avg): #replace
    #    return ((ct_data[round(((time-7368)/24+avg)*1000)+1]-ct_data[round((time-7368)/24*1000)])*1000/24)/(1000*avg)
    if (((time-0)/24)*1000) < len(ct_data): #replace
        return ((ct_data[round((time/24)*1000)+1]-ct_data[round(time/24*1000)])*1000/24)
    return 0 """
def ct_tau_gain(cts,time):
    if time < 66600:  #go to the end of ct_data rounded down to nearest time in days and multiply by 24 replace this number here so it doesnt go out of range
        cts = ct_data[round(time/24*1000)]
    else:
        cts = 3600
    return cts

def ct_rate(time):
    avg = 30 # calculates tau/hr of cts over an average of x days, changing this values will not affect results much
    if time < (66600-24*avg): #replace
        return ((ct_data[round((time/24+avg)*1000)+1]-ct_data[round(time/24*1000)])*1000/24)/(1000*avg)
    elif time < 66600: #replace
        return ((ct_data[round((time/24)*1000)+1]-ct_data[round(time/24*1000)])*1000/24)
    return 0

def calculate_rates(main_theory_rates, sigma,cts,time):
    #recalculates students after each publish based on total tau (essentially assuming you grad at every student), will be replace with accurate phi*tau data later
    tau_current = sum(main_theory_values)+cts
    #sigma = math.floor(sigma + (tau_current - tau_start) / 20.36)
    if (tau_current < 4580):
        sigma = math.floor(95 + (tau_current - 2050) / 16.86)
    elif (tau_current >= 4580 and tau_current < 7100):
        sigma = math.floor(245 + (tau_current - 4580) / 25.2)
    elif (tau_current >= 7100 and tau_current < 10150):
        sigma = math.floor(345 + (tau_current - 7070) / 20.33)
    elif (tau_current >= 10150):
        sigma = math.floor(495 + (tau_current - 10110) / 20)
    
    r9_boost = [(sigma / 20) ** 3, (sigma / 20) ** (3 / 10.2), (sigma / 20) ** 3, (sigma / 20) ** 2, (sigma / 20) ** 3,
            (sigma / 20), (sigma / 20) ** 3, (sigma / 20) ** 3]
    for i in range(len(main_theory_values)):
        main_theory_rates[i] = 2 ** -((main_theory_values[i] - scaled_values[i]) / decay[i]) * scaled[i] * r9_boost[i]
    

    with open(r"", "a") as file: #set absolute path of "main_theory_routing.txt"
        file.write(f"{sigma} ")
        for value in main_theory_values:
            file.write(f"{value:.3f} ")
        file.write(f"{sum(main_theory_values):.3f} {cts} {(sum(main_theory_values)+cts):.3f} {round(time / 24, 3)}\n")



def cash_in(main_theory_values, main_theory_rates, time, sigma,cts):
    while main_theory_rates[5] > main_theory_rates[1]:
    #while main_theory_values[5] < 1247: #if trying to minimize time turn disable above and turn on and set t6 e1 less than greedy value of t6
        calculate_rates(main_theory_rates, sigma,cts,time)
        overpush_rates = [main_theory_rates[0],
                              (main_theory_rates[1]),
                              main_theory_rates[2],
                              (main_theory_rates[3])*1.5,
                              main_theory_rates[4],
                              (main_theory_rates[5])*3,
                              main_theory_rates[6],
                              main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    
    while main_theory_rates[3] > main_theory_rates[1]:
    #while main_theory_values[3] < 1169: #if trying to minimize time turn disable line above and turn on and set t4 e1 less than greedy value of t4
        calculate_rates(main_theory_rates, sigma,cts,time)
        overpush_rates = [main_theory_rates[0],
                              (main_theory_rates[1]),
                              main_theory_rates[2],
                              (main_theory_rates[3])*1.5,
                              main_theory_rates[4],
                              (main_theory_rates[5]),
                              main_theory_rates[6],
                              main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    

    calculate_rates(main_theory_rates, sigma,cts,time)
    while main_theory_rates[2] > main_theory_rates[1]:
    #while sum(main_theory_values) + cts < 12552:

    #while sum(main_theory_values)+cts < 10110: #if trying to minimize time disable line above and set tau to greedy value of total tau
        calculate_rates(main_theory_rates, sigma,cts,time)
        fastest = main_theory_rates.index(max(main_theory_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)


    return time,cts

def greedy_strat(main_theory_values, main_theory_rates, time, sigma,cts):
    #while sum(main_theory_values)+cts < 12000: # set a stop condition
    #while cts < 3600:
    while time < (365*24) :
    #while main_theory_values[1] < 2000:
    #while sum(main_theory_values)+cts < 100000:
        calculate_rates(main_theory_rates, sigma,cts,time)
        fastest = main_theory_rates.index(max(main_theory_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)

    return time,cts
# normal overpush without cts
def overpush_strat(main_theory_values, main_theory_rates, time, sigma,cts):
    while sum(main_theory_values)+cts< 800:
    #while main_theory_values[1] < 705:
    #while cts < 2400:
        calculate_rates(main_theory_rates, sigma,cts,time)
        #if (sum(main_theory_values) <5900):
        overpush_rates = [main_theory_rates[0],
                            (main_theory_rates[1])*10.2,
                            main_theory_rates[2],
                            (main_theory_rates[3])*1.5,
                            main_theory_rates[4],
                            (main_theory_rates[5])*7,
                            main_theory_rates[6],
                            main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    #else:
        #time,cts = cash_in(main_theory_values, main_theory_rates, time, sigma,cts)
    return time,cts
# overpush accounting for cts rates (best results)
def overpush_strat_2(main_theory_values, main_theory_rates, time, sigma,cts):
    while (main_theory_values[1] < 800) :  # caps t2 otherwise it WILL push t2 to 780-800+ (if trying to minimize time set this t2 to e1 less than greedy t2)
        calculate_rates(main_theory_rates, sigma,cts,time)
        #print(main_theory_rates)
        overpush_rates = [main_theory_rates[0]+ct_rate(time),
                            ((main_theory_rates[1])+ct_rate(time))*10.2,
                            main_theory_rates[2]+ct_rate(time),
                            ((main_theory_rates[3])+ct_rate(time))*1.5,
                            main_theory_rates[4]+ct_rate(time),
                            ((main_theory_rates[5])+ct_rate(time))*3,
                            main_theory_rates[6]+ct_rate(time),
                            main_theory_rates[7]+ct_rate(time)]
        #print(overpush_rates)
        #print(ct_rate(time))
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
        #print(cts)

    #delayt2 = False # turn this on only if you want to delay a t2 push for later for practical reasons
    
    
    #begins optimal cash in (note, if trying to minimize time you need to manually test different cts limit )
    calculate_rates(main_theory_rates, sigma,cts,time)
    while (cts < 3600 and main_theory_rates[3] > main_theory_rates[1] and main_theory_rates[5] > main_theory_rates[1]) :
        calculate_rates(main_theory_rates, sigma,cts,time)
        overpush_rates = [main_theory_rates[0]+ct_rate(time),
                            ((main_theory_rates[1]))+ct_rate(time),
                            main_theory_rates[2]+ct_rate(time),
                            ((main_theory_rates[3])+ct_rate(time))*1.5,
                            main_theory_rates[4]+ct_rate(time),
                            ((main_theory_rates[5])+ct_rate(time))*3,
                            main_theory_rates[6]+ct_rate(time),
                            main_theory_rates[7]+ct_rate(time)]
        
        fastest = overpush_rates.index(max(overpush_rates))
        #if (time > 720) and (delayt2 == False): # set time in hours for how long to delay extra t2 push for
        #    fastest = 1
        #    delayt2 = True

        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)

    else:
        time,cts = cash_in(main_theory_values, main_theory_rates, time, sigma,cts)
        
        
    return time,cts

# drop everything but t2 strat
def overpush_strat_3(main_theory_values, main_theory_rates, time, sigma,cts):
    #while sum(main_theory_values)+cts< 10150:
    while main_theory_values[1] < 705:
        calculate_rates(main_theory_rates, sigma,cts,time)
        pub_time = pub_length[1] / main_theory_rates[1]
        main_theory_values[1] += pub_length[1]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    else:
        time,cts = cash_in(main_theory_values, main_theory_rates, time, sigma,cts)
    return time,cts

# custom overpush ratios
def overpush_strat_4(main_theory_values, main_theory_rates, time, sigma,cts):
    #while sum(main_theory_values)+cts< 10150:
    while main_theory_values[1] < 705:
        calculate_rates(main_theory_rates, sigma,cts,time)
        #if (sum(main_theory_values) <5900):
        overpush_rates = [main_theory_rates[0],
                            (main_theory_rates[1])*90,
                            main_theory_rates[2],
                            (main_theory_rates[3])*1.5,
                            main_theory_rates[4],
                            (main_theory_rates[5])*3.3,
                            main_theory_rates[6],
                            main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    
    while main_theory_values[5] < 1585:
        calculate_rates(main_theory_rates, sigma,cts,time)
        #if (sum(main_theory_values) <5900):
        overpush_rates = [main_theory_rates[0],
                            (main_theory_rates[1]),
                            main_theory_rates[2],
                            (main_theory_rates[3])*1.5,
                            main_theory_rates[4],
                            (main_theory_rates[5])*4.30,
                            main_theory_rates[6],
                            main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)
    
    while main_theory_values[3] < 950:
        calculate_rates(main_theory_rates, sigma,cts,time)
        #if (sum(main_theory_values) <5900):
        overpush_rates = [main_theory_rates[0],
                            (main_theory_rates[1]),
                            main_theory_rates[2],
                            (main_theory_rates[3])*1.4,
                            main_theory_rates[4],
                            (main_theory_rates[5]),
                            main_theory_rates[6],
                            main_theory_rates[7]]
        
        fastest = overpush_rates.index(max(overpush_rates))
        pub_time = pub_length[fastest] / main_theory_rates[fastest]
        main_theory_values[fastest] += pub_length[fastest]
        time += pub_time
        cts = ct_tau_gain(cts,time)


    else:
        time,cts = cash_in(main_theory_values, main_theory_rates, time, sigma,cts)
    return time,cts



def extract_second_column(file_path):

    ct_data = []
    
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()  
            if len(parts) == 2:  
                try:
                    value = float(parts[1])  
                    ct_data.append(value)  
                except ValueError:
                    print(f"Warning: Could not convert '{parts[1]}' to float.")
    
    return ct_data

# Example usage
file_path = r"" #set absolute path of ct_tau_lookup_table.txt

ct_data = extract_second_column(file_path)

#time,cts = greedy_strat(main_theory_values, main_theory_rates, time, sigma,cts)
time,cts = overpush_strat_2(main_theory_values, main_theory_rates, time, sigma,cts)

tau_current = sum(main_theory_values)+cts
#sigma = math.floor(sigma + (tau_current - tau_start) / 20.36)
if (tau_current < 4580):
    sigma = math.floor(95 + (tau_current - 2050) / 16.86)
elif (tau_current >= 4580 and tau_current < 7100):
    sigma = math.floor(245 + (tau_current - 4580) / 25.2)
elif (tau_current >= 7100 and tau_current < 10150):
    sigma = math.floor(345 + (tau_current - 7070) / 20.33)
elif (tau_current >= 10150):
    sigma = math.floor(495 + (tau_current - 10110) / 20)

print(sigma, " ", end="")
for value in main_theory_values:
    print("{:.3f}".format(value), end=" ")
print(" {:.3f}".format(sum(main_theory_values)), " ", cts, " ", round(time/24,3))

for rate in main_theory_rates:
    print("{:.5f}".format(rate), end=" ")

print("Total tau", sum(main_theory_values)+cts)