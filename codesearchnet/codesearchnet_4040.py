def generate(self, nb_steps=100, averaging=50, rescale=True):
        """Generate data from an FCM containing cycles."""
        if self.cfunctions is None:
            self.init_variables()
        new_df = pd.DataFrame()
        causes = [[c for c in np.nonzero(self.adjacency_matrix[:, j])[0]]
                  for j in range(self.nodes)]
        values = [[] for i in range(self.nodes)]

        for i in range(nb_steps):
            for j in range(self.nodes):
                new_df["V" + str(j)] = self.cfunctions[j](self.data.iloc[:, causes[j]].values)[:, 0]
                if rescale:
                    new_df["V" + str(j)] = scale(new_df["V" + str(j)])
                if i > nb_steps-averaging:
                    values[j].append(new_df["V" + str(j)])
            self.data = new_df
        self.data = pd.DataFrame(np.array([np.mean(values[i], axis=0)
                                           for i in range(self.nodes)]).transpose(),
                                 columns=["V{}".format(j) for j in range(self.nodes)])

        return self.g, self.data