def calculate_derivative(self, T, method, order=1):
        r'''Method to calculate a derivative of a property with respect to 
        temperature, of a given order  using a specified method. Uses SciPy's 
        derivative function, with a delta of 1E-6 K and a number of points 
        equal to 2*order + 1.

        This method can be overwritten by subclasses who may perfer to add
        analytical methods for some or all methods as this is much faster.

        If the calculation does not succeed, returns the actual error
        encountered.

        Parameters
        ----------
        T : float
            Temperature at which to calculate the derivative, [K]
        method : str
            Method for which to find the derivative
        order : int
            Order of the derivative, >= 1

        Returns
        -------
        derivative : float
            Calculated derivative property, [`units/K^order`]
        '''
        return derivative(self.calculate, T, dx=1e-6, args=[method], n=order, order=1+order*2)