def init_variables(self, verbose=False):
        """Redefine the causes of the graph."""
        # Resetting adjacency matrix
        for i in range(self.nodes):
            for j in np.random.choice(range(self.nodes),
                                      np.random.randint(
                                          0, self.parents_max + 1),
                                      replace=False):
                if i != j:
                    self.adjacency_matrix[j, i] = 1

        try:
            assert any([sum(self.adjacency_matrix[:, i]) ==
                        self.parents_max for i in range(self.nodes)])
            self.g = nx.DiGraph(self.adjacency_matrix)
            assert list(nx.simple_cycles(self.g))
            assert any(len(i) == 2 for i in nx.simple_cycles(self.g))

        except AssertionError:
            if verbose:
                print("Regenerating, graph non valid...")
            self.init_variables()

        if verbose:
            print("Matrix generated ! \
              Number of cycles: {}".format(len(list(nx.simple_cycles(self.g)))))

        for i in range(self.nodes):
            self.data.iloc[:, i] = scale(self.initial_generator(self.points))

        # Mechanisms
        self.cfunctions = [self.mechanism(int(sum(self.adjacency_matrix[:, i])),
                                          self.points, self.noise, noise_coeff=self.noise_coeff) for i in range(self.nodes)]