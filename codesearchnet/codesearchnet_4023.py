def mechanism(self, causes):
        """Mechanism function."""
        result = np.zeros((self.points, 1))
        for i in range(self.points):
            pre_add_effect = 0
            for c in range(causes.shape[1]):
                pre_add_effect += causes[i, c]
            pre_add_effect += self.noise[i]

            result[i, 0] = self.a * self.b * \
                (pre_add_effect + self.c)/(1 + abs(self.b*(pre_add_effect + self.c)))

        return result