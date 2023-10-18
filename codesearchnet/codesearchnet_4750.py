def _mutation(chromosomes, count_clusters, count_gen_for_mutation, coeff_mutation_count):
        """!
        @brief Mutation procedure.
        
        """

        # Count gens in Chromosome
        count_gens = len(chromosomes[0])

        # Get random chromosomes for mutation
        random_idx_chromosomes = np.array(range(len(chromosomes)))
        np.random.shuffle(random_idx_chromosomes)

        #
        for _idx_chromosome in range(int(len(random_idx_chromosomes) * coeff_mutation_count)):

            #
            for _ in range(count_gen_for_mutation):

                # Get random gen
                gen_num = np.random.randint(count_gens)

                # Set random cluster
                chromosomes[random_idx_chromosomes[_idx_chromosome]][gen_num] = np.random.randint(count_clusters)