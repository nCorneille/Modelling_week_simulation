import numpy as np
from numba import njit


class SequenceAnalyser:
    @staticmethod
    def get_first_element(conditioned_data: np.array(bool)) -> int:
        """
        :param conditioned_data: some condition on an np.array
        :return: the first element of condition_data which is True, or len(conditioned_data) if every element is False
        """
        if not np.any(conditioned_data):
            return len(conditioned_data)
        else:
            return np.argmax(conditioned_data)

    @staticmethod
    def get_first_sequence(conditioned_data: np.array(bool), n: int) -> int:
        """
        Generalizes get_first_element to sequences of consecutive conditions.
        Based on code by Henry Shackleton (https://www.javaer101.com/en/article/1008280.html)
        :param conditioned_data: Set of conditioned observations
        :param n: number of points
        :return: first index for which conditioned_data[index:index+n] are all True
        """

        out = len(conditioned_data)
        for i in range(out - n + 1):
            found = True
            for j in range(n):
                if not conditioned_data[i + j]:
                    found = False
                    break
            if found:
                out = i
                break

        return out

    @staticmethod
    def get_length_true_sequences(conditioned_data, minimum_length):
        length = len(conditioned_data)
        out_lengths = []
        out_indices = []

        sequence_length = 0
        for i in range(length):
            if conditioned_data[i] and i != length-1:
                sequence_length += 1
            elif (not(conditioned_data[i]) and sequence_length != 0) or i == length-1:
                if sequence_length >= minimum_length:
                    out_lengths.append(sequence_length)
                    out_indices.append(i-sequence_length)
                sequence_length = 0

        return out_lengths, out_indices

