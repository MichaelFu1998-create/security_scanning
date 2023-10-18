def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g.
          {'CO': 0.25, 'CO2': 0.25, 'N2': 0.25, 'O2': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above
        that are used to describe the state of the material.
        """

        def phi(i, j, mu_i, mu_j):
            M_i = M(i)
            M_j = M(j)

            result = (1.0 + (mu_i / mu_j)**0.5 * (M_j / M_i)**0.25)**2.0
            result /= (4.0 / sqrt(2.0))
            result /= (1.0 + M_i / M_j)**0.5

            return result

        T = state['T']
        x = state['x']

        # normalise mole fractions
        x_total = sum([
            x for compound, x in x.items()
            if compound in materials])
        x = {
            compound: x[compound]/x_total
            for compound in x.keys()
            if compound in materials}

        result = 0.0  # Pa.s
        mu = {i: materials[i].mu(T=T) for i in x.keys()}
        for i in x.keys():
            sum_i = 0.0
            for j in x.keys():
                if j == i: continue
                sum_i += x[j] * phi(i, j, mu[i], mu[j])

            result += x[i] * mu[i] / (x[i] + sum_i)

        return result