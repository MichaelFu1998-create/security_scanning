def mechanism(self, x):
        """Mechanism function."""
        result = np.\
            zeros((self.points, 1))
        for i in range(self.points):

            result[i, 0] = self.a * self.b * (x[i] + self.c) / (1 + abs(self.b * (x[i] + self.c)))

        return result + self.noise