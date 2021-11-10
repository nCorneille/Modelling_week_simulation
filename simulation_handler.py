from matrix_handler import *


class TransitionHandler:
    def __init__(self, markov_model: MarkovChainModel, supply_per_machine, start_state):
        self.markov_model = markov_model
        self.transition_matrix = markov_model.matrix
        self.cur_state = start_state
        self.supply_per_machine = supply_per_machine

    def choose_next_state(self, current_state: int, m: int):
        row = self.transition_matrix
        next_state = np.random.choice([i for i in range(m)], 1, p=[row[current_state, i] for i in range(m)])[0]
        return next_state

    def update_state(self, m):
        self.cur_state = self.choose_next_state(self.cur_state, m)

    def transition_simulation(self, start_state, iterations):
        i = 0
        cur_state = start_state
        states = [start_state]

        while i < iterations:
            next_state = self.choose_next_state(cur_state)[0]
            cur_state = next_state

            states.append(cur_state)
            i += 1

        return states


class BufferSimulationHandler():
    def __init__(self, markov_models, maximum_size=1 << 31, minimum_size=0):
        self.markov_models = markov_models
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size

    def buffer_simulation(self, start_state, init_buffer, max_iterations, demand):
        cur_buffer = init_buffer

        buffer = [cur_buffer]
        states = []
        states.append([model.cur_state for model in self.markov_models])
        i = 0

        while i < max_iterations:
            for model in self.markov_models:
                cur_buffer += model.cur_state * model.supply_per_machine
                model.update_state(model.transition_matrix.shape[0])

            cur_buffer -= demand[i % len(demand)]
            cur_buffer = max(self.minimum_size, cur_buffer)
            cur_buffer = min(self.maximum_size, cur_buffer)

            buffer.append(cur_buffer)
            states.append([model.cur_state for model in self.markov_models])

            i += 1

        return states, buffer
