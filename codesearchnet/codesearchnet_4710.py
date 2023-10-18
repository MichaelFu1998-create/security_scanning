def set_last_value_to_one(probabilities):
        """!
        @brief Update the last same probabilities to one.
        @details All values of probability list equals to the last element are set to 1.
        
        """

        # Start from the last elem
        back_idx = - 1

        # All values equal to the last elem should be set to 1
        last_val = probabilities[back_idx]

        # for all elements or if a elem not equal to the last elem
        for _ in range(-1, -len(probabilities) - 1):
            if probabilities[back_idx] == last_val:
                probabilities[back_idx] = 1
            else:
                break