import os
import csv

from simulation_handler import *
from matrix_handler import *
from sequence_analysis import *
from fine_handler import *


def csv_reader(filename):
    filename += ".csv"
    out = []

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            out.append(row)

    return np.array(out).flatten().astype(float)


def fine(T):
    return 0 if T < 8 else 35 + np.floor((T - 8) / 4) * 20


# Failure rates based on Badami et al.
# Boilers:
# lambda = 5 * 10^-3
# mu = 1
#
# Pumps:
# lambda = 1 * 10^-5
# mu = 0.083


demand_data = csv_reader("demand_data")

MAX_ITER = 24 * 365
START_BUFFER = 30000
MAX_BUFFER = 0.0011 * 30 * 2 * 750 * 1000 # = 49500

def HEAT_PUMP_POLICY(current_buffer, maximum_buffer):
    r = current_buffer / maximum_buffer
    return 1 if r <= 0.95 else 0
    # return 1

# MACHINE 1: HEAT PUMPS
MACHINE_1_AMOUNT = 5
MACHINE_1_FAIL_RATE = 1e-5
MACHINE_1_REPAIR_RATE = 0.083
MACHINE_1_START_STATE = MACHINE_1_AMOUNT
MACHINE_1_POWER = 1800

machine_1_mm = MarkovChainModel()
machine_1_matrix = make_matrix(MACHINE_1_AMOUNT, MACHINE_1_FAIL_RATE, MACHINE_1_REPAIR_RATE)
machine_1_mm.change_matrix(machine_1_matrix)
machine_1_transition_handler = TransitionHandler(machine_1_mm, MACHINE_1_POWER, MACHINE_1_AMOUNT, HEAT_PUMP_POLICY)


def GAS_BOILER_POLICY(current_buffer, maximum_buffer):
    r = current_buffer / maximum_buffer
    if r <= 0.4:
        return 1
    elif 0.4 < r <= 0.75:
        return 0.5
    else:
        return 0


def CHP_POLICY(current_buffer, maximum_buffer):
    r = current_buffer / maximum_buffer
    if r > 0.9:
        return 0
    elif 0.9 >= r > 0.85:
        return 0.5
    else:
        return 1


# MACHINE 2: CHP
MACHINE_2_AMOUNT = 4
MACHINE_2_FAIL_RATE = 1.65e-3
MACHINE_2_REPAIR_RATE = 0.106
MACHINE_2_START_STATE = MACHINE_2_AMOUNT
MACHINE_2_POWER = 900 * 0.2

machine_2_mm = MarkovChainModel()
machine_2_matrix = make_matrix(MACHINE_2_AMOUNT, MACHINE_2_FAIL_RATE, MACHINE_2_REPAIR_RATE)
machine_2_mm.change_matrix(machine_2_matrix)
machine_2_transition_handler = TransitionHandler(machine_2_mm, MACHINE_2_POWER, MACHINE_2_AMOUNT, CHP_POLICY)

# MACHINE 3: GAS BOILERS
MACHINE_3_AMOUNT = 3
MACHINE_3_FAIL_RATE = 0
MACHINE_3_REPAIR_RATE = 1
MACHINE_3_START_STATE = MACHINE_3_AMOUNT
MACHINE_3_POWER = 6000

machine_3_mm = MarkovChainModel()
machine_3_matrix = make_matrix(MACHINE_3_AMOUNT, MACHINE_3_FAIL_RATE, MACHINE_3_REPAIR_RATE)
machine_3_mm.change_matrix(machine_3_matrix)
machine_3_transition_handler = TransitionHandler(machine_3_mm, MACHINE_3_POWER, MACHINE_3_AMOUNT, GAS_BOILER_POLICY)

machines = [machine_1_transition_handler, machine_2_transition_handler, machine_3_transition_handler]
buffer_simulation_handler = BufferSimulationHandler(machines, MAX_BUFFER)
# buffer = buffer_simulation_handler.buffer_simulation(START_BUFFER, MAX_ITER, demand_data)
# print(buffer[0])
# print(buffer[1])
#
# L = SequenceAnalyser.get_length_true_sequences(np.array(buffer[1]) == 0, 1)
#
# print(L[0])
# print(FineHandler(lambda x: x).to_days_between(L[0], L[1]))
#
# print(FineHandler(fine).calculate_fine(L[0], L[1]))

buffer = buffer_simulation_handler.buffer_simulation(START_BUFFER, MAX_ITER, demand_data)
L = SequenceAnalyser.get_length_true_sequences(np.array(buffer[1]) == 0, 1)
fail_rates = [MACHINE_1_FAIL_RATE]
fines = [FineHandler(fine).calculate_fine(L[0], L[1])]

#MACHINE_3_FAIL_RATE += 0.25

for i in range(100):
    print(fines[i])
    print(i)
    MACHINE_1_FAIL_RATE += 5e-4
    #MACHINE_2_FAIL_RATE += 1.65e-3
    #MACHINE_3_FAIL_RATE += 0.005

    fail_rates.append(MACHINE_1_FAIL_RATE)

    fine_list = []
    for j in range(10):
        print(f"|-{j}")
        machine_1_matrix = make_matrix(MACHINE_1_AMOUNT, MACHINE_1_FAIL_RATE, MACHINE_1_REPAIR_RATE)
        machine_1_mm.change_matrix(machine_1_matrix)
        machine_1_transition_handler = TransitionHandler(machine_1_mm, MACHINE_1_POWER, MACHINE_1_AMOUNT,
                                                         HEAT_PUMP_POLICY)

        machine_2_matrix = make_matrix(MACHINE_2_AMOUNT, MACHINE_2_FAIL_RATE, MACHINE_2_REPAIR_RATE)
        machine_2_mm.change_matrix(machine_2_matrix)
        machine_2_transition_handler = TransitionHandler(machine_2_mm, MACHINE_2_POWER, MACHINE_2_AMOUNT, GAS_BOILER_POLICY)

        machine_3_matrix = make_matrix(MACHINE_3_AMOUNT, MACHINE_3_FAIL_RATE, MACHINE_3_REPAIR_RATE)
        machine_3_mm.change_matrix(machine_3_matrix)
        machine_3_transition_handler = TransitionHandler(machine_3_mm, MACHINE_3_POWER, MACHINE_3_AMOUNT, GAS_BOILER_POLICY)

        machines = [machine_1_transition_handler, machine_2_transition_handler, machine_3_transition_handler]
        buffer_simulation_handler = BufferSimulationHandler(machines, MAX_BUFFER)

        buffer = buffer_simulation_handler.buffer_simulation(START_BUFFER, MAX_ITER, demand_data)
        L = SequenceAnalyser.get_length_true_sequences(np.array(buffer[1]) == 0, 1)
        fine_list.append(FineHandler(fine).calculate_fine(L[0], L[1]))
    fines.append(np.mean(fine_list))

f = open("output.csv", "w")
writer = csv.writer(f)
for i in range(len(fines)):
    print(f"{fail_rates[i]},{fines[i]}")
    writer.writerow([fail_rates[i], fines[i]])
f.close()
