def mechanism(self, x):
        """Mechanism function."""
        layers = []

        layers.append(th.nn.modules.Linear(self.n_causes+1, self.nh))
        layers.append(th.nn.Tanh())
        layers.append(th.nn.modules.Linear(self.nh, 1))

        self.layers = th.nn.Sequential(*layers)

        data = x.astype('float32')
        data = th.from_numpy(data)

        return np.reshape(self.layers(data).data, (x.shape[0],))