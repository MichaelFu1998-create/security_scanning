def calculate_bin_boundary(self, bb):
        """Calculate the adc value that corresponds to a specific bin boundary diameter in microns.

            :param bb: Bin Boundary in microns

            :type bb: float

            :rtype: int
        """

        return min(enumerate(OPC_LOOKUP), key = lambda x: abs(x[1] - bb))[0]