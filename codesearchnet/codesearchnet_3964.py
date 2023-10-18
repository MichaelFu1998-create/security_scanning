def forward(self):
        """Generate according to the topological order of the graph."""
        self.noise.data.normal_()
        if not self.confounding:
            for i in self.topological_order:
                self.generated[i] = self.blocks[i](th.cat([v for c in [
                                                   [self.generated[j] for j in np.nonzero(self.adjacency_matrix[:, i])[0]],
                                                   [self.noise[:, [i]]]] for v in c], 1))
        else:
            for i in self.topological_order:
                self.generated[i] = self.blocks[i](th.cat([v for c in [
                                                   [self.generated[j] for j in np.nonzero(self.adjacency_matrix[:, i])[0]],
                                                   [self.corr_noise[min(i, j), max(i, j)] for j in np.nonzero(self.i_adj_matrix[:, i])[0]]
                                                   [self.noise[:, [i]]]] for v in c], 1))
        return th.cat(self.generated, 1)