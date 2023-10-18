def _calc_a(self, y_C, y_H, y_O, y_N, y_S):
        """
        Calculate the mean atomic weight for the specified element mass
        fractions.
        
        :param y_C: Carbon mass fraction
        :param y_H: Hydrogen mass fraction
        :param y_O: Oxygen mass fraction
        :param y_N: Nitrogen mass fraction
        :param y_S: Sulphur mass fraction
       
        :returns: [kg/kmol] mean atomic weight

        See equation at bottom of page 538 of Merrick1983a.
        """

        return 1 / (y_C/mm("C") + y_H/mm("H") + y_O/mm("O") + y_N/mm("N") +
                    y_S/mm("S"))