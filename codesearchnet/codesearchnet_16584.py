def inquire(self):
        """Maps to fortran CDF_Inquire.

        Assigns parameters returned by CDF_Inquire
        to pysatCDF instance. Not intended
        for regular direct use by user.

        """

        name = copy.deepcopy(self.fname)
        stats = fortran_cdf.inquire(name)

        # break out fortran output into something meaningful
        status = stats[0]
        if status == 0:
            self._num_dims = stats[1]
            self._dim_sizes = stats[2]
            self._encoding = stats[3]
            self._majority = stats[4]
            self._max_rec = stats[5]
            self._num_r_vars = stats[6]
            self._num_z_vars = stats[7]
            self._num_attrs = stats[8]
        else:
            raise IOError(fortran_cdf.statusreporter(status))