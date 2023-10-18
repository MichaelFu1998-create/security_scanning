def solve_prop(self, goal, reset_method=True):
        r'''Method to solve for the temperature at which a property is at a
        specified value. `T_dependent_property` is used to calculate the value
        of the property as a function of temperature; if `reset_method` is True,
        the best method is used at each temperature as the solver seeks a
        solution. This slows the solution moderately.

        Checks the given property value with `test_property_validity` first
        and raises an exception if it is not valid. Requires that Tmin and
        Tmax have been set to know what range to search within.

        Search is performed with the brenth solver from SciPy.

        Parameters
        ----------
        goal : float
            Propoerty value desired, [`units`]
        reset_method : bool
            Whether or not to reset the method as the solver searches

        Returns
        -------
        T : float
            Temperature at which the property is the specified value [K]
        '''
        if self.Tmin is None or self.Tmax is None:
            raise Exception('Both a minimum and a maximum value are not present indicating there is not enough data for temperature dependency.')
        if not self.test_property_validity(goal):
            raise Exception('Input property is not considered plausible; no method would calculate it.')

        def error(T):
            if reset_method:
                self.method = None
            return self.T_dependent_property(T) - goal
        try:
            return brenth(error, self.Tmin, self.Tmax)
        except ValueError:
            raise Exception('To within the implemented temperature range, it is not possible to calculate the desired value.')