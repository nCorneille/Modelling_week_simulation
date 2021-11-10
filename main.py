import os

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
    return 0 if T < 8 else 35 + np.floor((T-8)/4) * 20

#Failure rates based on Badami et al.
#Boilers:
#lambda = 5 * 10^-3
#mu = 1
#
#Pumps:
#lambda = 1 * 10^-5
#mu = 0.083


demand_data = csv_reader("demand_data")

model_2_mch = MarkovChainModel("matrix_2",
                              {"lambda": "5e-3", "mu": "1", "exp": "exp"},
                              {"exp": np.exp})

model_2_mch_sim = TransitionHandler(model_2_mch)

MAX_ITER = 24 * 365
START_BUFFER = 100000
MCH_POWER = np.mean(demand_data)/3 * 2
START_STATE = 2

buffer_model_2_mch = BufferSimulationHandler(model_2_mch)
buffer = buffer_model_2_mch.buffer_simulation(START_STATE, START_BUFFER, MAX_ITER, demand_data, MCH_POWER)
print(buffer[0])
print(buffer[1])

L = SequenceAnalyser.get_length_true_sequences(np.array(buffer[1]) == 0, 1)

print(L[0])
print(FineHandler(lambda x: x).to_days_between(L[0], L[1]))

print(FineHandler(fine).calculate_fine(L[0],L[1]))