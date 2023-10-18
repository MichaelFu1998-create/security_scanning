def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param y: [mass fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        y = state['y']
        x = amount_fractions(y)
        return super().calculate(T=T, x=x)