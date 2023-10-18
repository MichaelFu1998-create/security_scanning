def get_uniform(probabilities):
        """!
        @brief Returns index in probabilities.

        @param[in] probabilities (list): List with segments in increasing sequence with val in [0, 1],
                   for example, [0 0.1 0.2 0.3 1.0].
        """

        # Initialize return value
        res_idx = None

        # Get random num in range [0, 1)
        random_num = np.random.rand()

        # Find segment with  val1 < random_num < val2
        for _idx in range(len(probabilities)):
            if random_num < probabilities[_idx]:
                res_idx = _idx
                break

        if res_idx is None:
            print('Probabilities : ', probabilities)
            raise AttributeError("'probabilities' should contain 1 as the end of last segment(s)")

        return res_idx