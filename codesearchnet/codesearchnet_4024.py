def mechanism(self, x, par):
        """Mechanism function."""
        list_coeff = self.polycause[par]
        result = np.zeros((self.points, 1))
        for i in range(self.points):
            for j in range(self.d+1):
                result[i, 0] += list_coeff[j]*np.power(x[i], j)
            result[i, 0] = min(result[i, 0], 1)
            result[i, 0] = max(result[i, 0], -1)

        return result