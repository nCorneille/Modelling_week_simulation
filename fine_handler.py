ONE_YEAR = 24 * 365

class FineHandler:
    def __init__(self, fine_function):
        self.fine_function = fine_function

    def to_days_between(self, interval_lengths, interval_indices):
        assert (len(interval_lengths) == len(interval_indices))
        if len(interval_indices) == 0:
            return []

        out = [interval_indices[0]]

        for i in range(1, len(interval_lengths)):
            out.append(interval_indices[i] - interval_lengths[i-1] - interval_indices[i-1])

        return out

    def calculate_fine(self, interval_lengths, interval_indices):
        assert(len(interval_lengths) == len(interval_indices))
        if len(interval_lengths) == 0:
            return 0

        should_skip = True
        days_between = self.to_days_between(interval_lengths, interval_indices)

        fine = 0
        for i in range(len(interval_lengths)):
            if days_between[i] > ONE_YEAR:
                should_skip = True

            if should_skip:
                should_skip = False
                if interval_lengths[i] < 24:
                    continue

            fine += self.fine_function(interval_lengths[i])
        return fine


