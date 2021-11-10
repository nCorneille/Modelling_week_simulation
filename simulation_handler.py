from matrix_handler import *


class TransitionHandler:
    def __init__(self, markov_model: MarkovChainModel):
        self.markov_model = markov_model
        self.transition_matrix = evaluate_model(markov_model.matrix, markov_model.values)

    def choose_next_state(self, current_state: int):
        row = self.transition_matrix[current_state]
        next_state = np.random.choice([0, 1, 2], 1, p=[row[0, 0], row[0, 1], row[0, 2]])
        return next_state

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


class BufferSimulationHandler(TransitionHandler):
    def __init__(self, markov_model: MarkovChainModel, maximum_size=1 << 31, minimum_size=0):
        super().__init__(markov_model)
        self.minimum_size = minimum_size
        self.maximum_size = maximum_size

    def buffer_simulation(self, start_state, init_buffer, max_iterations, demand, supply_per_machine):
        cur_state = start_state
        cur_buffer = init_buffer

        buffer = [cur_buffer]
        states = [start_state]
        i = 0

        while i < max_iterations:
            cur_buffer += cur_state * supply_per_machine - demand[i % max_iterations]
            cur_state = self.choose_next_state(cur_state)[0]

            cur_buffer = max(self.minimum_size, cur_buffer)
            cur_buffer = min(self.maximum_size, cur_buffer)

            buffer.append(cur_buffer)
            states.append(cur_state)

            i += 1

        return states, buffer
