def _get_crossover_mask(mask_length):
        """!
        @brief Crossover mask to crossover a pair of chromosomes.
        
        @param[in] mask_length (uint): Length of the mask.
        
        """

        # Initialize mask
        mask = np.zeros(mask_length)

        # Set a half of array to 1
        mask[:int(int(mask_length) / 2)] = 1

        # Random shuffle
        np.random.shuffle(mask)

        return mask