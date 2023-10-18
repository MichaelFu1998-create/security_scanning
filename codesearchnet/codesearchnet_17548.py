def calculate(self, **state):
        """
        Calculate the density at the specified temperature, pressure, and
        composition.

        :param T: [K] temperature
        :param P: [Pa] pressure
        :param x: [mole fraction] dictionary of compounds and mole fractions

        :returns: [kg/m3] density

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """
        super().calculate(**state)
        mm_average = 0.0
        for compound, molefraction in state["x"].items():
            mm_average += molefraction * mm(compound)
        mm_average /= 1000.0

        return mm_average * state["P"] / R / state["T"]