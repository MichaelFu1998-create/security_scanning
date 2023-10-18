def calc_probability_vector(fitness):
        """!
        """

        if len(fitness) == 0:
            raise AttributeError("Has no any fitness functions.")

        # Get 1/fitness function
        inv_fitness = np.zeros(len(fitness))

        #
        for _idx in range(len(inv_fitness)):

            if fitness[_idx] != 0.0:
                inv_fitness[_idx] = 1.0 / fitness[_idx]
            else:
                inv_fitness[_idx] = 0.0

        # Initialize vector
        prob = np.zeros(len(fitness))

        # Initialize first element
        prob[0] = inv_fitness[0]

        # Accumulate values in probability vector
        for _idx in range(1, len(inv_fitness)):
            prob[_idx] = prob[_idx - 1] + inv_fitness[_idx]

        # Normalize
        prob /= prob[-1]

        ga_math.set_last_value_to_one(prob)

        return prob