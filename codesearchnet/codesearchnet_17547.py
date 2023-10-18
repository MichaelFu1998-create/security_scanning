def calculate(self, **state):
        """
        Calculate the density at the specified temperature.

        :param T: [K] temperature

        :returns: [kg/m3] density

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        return self.mm * self.P / R / state["T"]