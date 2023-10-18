def _crossover(chromosomes):
        """!
        @brief Crossover procedure.
        
        """

        # Get pairs to Crossover
        pairs_to_crossover = np.array(range(len(chromosomes)))

        # Set random pairs
        np.random.shuffle(pairs_to_crossover)

        # Index offset ( pairs_to_crossover split into 2 parts : [V1, V2, .. | P1, P2, ...] crossover between V<->P)
        offset_in_pair = int(len(pairs_to_crossover) / 2)

        # For each pair
        for _idx in range(offset_in_pair):

            # Generate random mask for crossover
            crossover_mask = genetic_algorithm._get_crossover_mask(len(chromosomes[_idx]))

            # Crossover a pair
            genetic_algorithm._crossover_a_pair(chromosomes[pairs_to_crossover[_idx]],
                                                chromosomes[pairs_to_crossover[_idx + offset_in_pair]],
                                                crossover_mask)