def init_variables(self, verbose=False):
        """Redefine the causes of the graph."""
        for j in range(1, self.nodes):
            nb_parents = np.random.randint(0, min([self.parents_max, j])+1)
            for i in np.random.choice(range(0, j), nb_parents, replace=False):
                self.adjacency_matrix[i, j] = 1

        try:
            self.g = nx.DiGraph(self.adjacency_matrix)
            assert not list(nx.simple_cycles(self.g))

        except AssertionError:
            if verbose:
                print("Regenerating, graph non valid...")
            self.init_variables()

        # Mechanisms
        self.cfunctions = [self.mechanism(int(sum(self.adjacency_matrix[:, i])),
                                          self.points, self.noise, noise_coeff=self.noise_coeff)
                           if sum(self.adjacency_matrix[:, i])
                           else self.initial_generator for i in range(self.nodes)]