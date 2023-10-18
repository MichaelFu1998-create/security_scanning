def generate(self, rescale=True):
        """Generate data from an FCM containing cycles."""
        if self.cfunctions is None:
            self.init_variables()

        for i in nx.topological_sort(self.g):
            # Root cause

            if not sum(self.adjacency_matrix[:, i]):
                self.data['V{}'.format(i)] = self.cfunctions[i](self.points)
            # Generating causes
            else:
                self.data['V{}'.format(i)] = self.cfunctions[i](self.data.iloc[:, self.adjacency_matrix[:, i].nonzero()[0]].values)
            if rescale:
                self.data['V{}'.format(i)] = scale(self.data['V{}'.format(i)].values)

        return self.g, self.data