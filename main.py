import os

from simulation_handler import *
from matrix_handler import *
from sequence_analysis import *




#prev_dir = os.path.dirname(__file__) + "/../"

#Failure rates based on Badami et al.
#Boilers:
#lambda = 5 * 10^-3
#mu = 1
#
#Pumps:
#lambda = 1 * 10^-5
#mu = 0.083

model_2_mch = MarkovChainModel("matrix_2",
                              {"lambda": "1", "mu": "1", "exp": "exp"},
                              {"exp": np.exp})

model_2_mch_sim = TransitionHandler(model_2_mch)
print(model_2_mch_sim.choose_next_state(1))
print(model_2_mch_sim.transition_matrix)

states = model_2_mch_sim.transition_simulation(0, 1000)
#print((np.array(states) == 0).astype(int))
#amount_of_zero = np.sum((np.array(states) == 0).astype(int))
#print(amount_of_zero/1001)

buffer_model_2_mch = BufferSimulationHandler(model_2_mch)
buffer = buffer_model_2_mch.buffer_simulation(2, 0, 1000, 1, 1)
print(buffer[0])
print(buffer[1])
print(SequenceAnalyser.get_first_sequence(np.array(buffer[1]) == 0, 2))