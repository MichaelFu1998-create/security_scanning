def calculate(self, **state):
        """
        Calculate dynamic viscosity at the specified temperature and
        composition:

        :param T: [K] temperature
        :param x: [mole fraction] composition dictionary , e.g. \
        {'SiO2': 0.25, 'CaO': 0.25, 'MgO': 0.25, 'FeO': 0.25}

        :returns: [Pa.s] dynamic viscosity

        The **state parameter contains the keyword argument(s) specified above\
        that are used to describe the state of the material.
        """

        T = state['T']
        x = state['x']

        # normalise mole fractions
        x_total = sum(x.values())
        x = {compound: x[compound]/x_total for compound in x.keys()}

        xg = x.get('SiO2', .00) + x.get('P2O5', 0.0)
        xm = x.get('CaO', 0.0) + x.get('MgO', 0.0) + x.get('Na2O', 0.0) + \
            x.get('K2O', 0.0) + 3.0*x.get('CaF2', 0.0) + x.get('FeO', 0.0) + \
            x.get('MnO', 0.0) + 2.0*x.get('TiO2', 0.0) + 2.0*x.get('ZrO2', 0.0)

        xa = x.get('Al2O3', 0.0) + x.get('Fe2O3', 0.0) + x.get('B2O3', 0.0)

        # Note 2*XFeO1.5 = XFe2O3

        norm = 1.0 + x.get('CaF2', 0.0) + x.get('Fe2O3', 0.0) + \
            x.get('TiO2', 0.0) + x.get('ZrO2', 0.0)

        xg_norm = xg / norm
        xm_norm = xm / norm
        xa_norm = xa / norm

        alpha = xm_norm / (xm_norm + xa_norm)

        B0 = 13.8 + 39.9355*alpha - 44.049*alpha**2.0
        B1 = 30.481 - 117.1505*alpha + 129.9978*alpha**2.0
        B2 = -40.9429 + 234.0846*alpha - 300.04*alpha**2.0
        B3 = 60.7619 - 153.9276*alpha + 211.1616*alpha**2.0

        B = B0 + B1*xg_norm + B2*xg_norm**2.0 + B3*xg_norm**3.0

        A = exp(-0.2693*B - 11.6725)

        result = A*T*exp(1000.0*B/T)  # [P]

        return result / 10.0