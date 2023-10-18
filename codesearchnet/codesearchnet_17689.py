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

        mu = {i: materials[i].mu(T=T) for i in x.keys()}

        result = sum([mu[i] * x[i] * sqrt(M(i)) for i in x.keys()])
        result /= sum([x[i] * sqrt(M(i)) for i in x.keys()])

        return result