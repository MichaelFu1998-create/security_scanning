def alpha(self, **state):
        """
        Calculate the alpha value given the material state.

        :param **state: material state

        :returns: float
        """

        return self.k(**state) / self.rho(**state) / self.Cp(**state)