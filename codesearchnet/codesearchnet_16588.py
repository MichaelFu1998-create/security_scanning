def _process_return_multi_z(self, data, names, dim_sizes):
        """process and attach data from fortran_cdf.get_multi_*"""
        # process data
        d1 = 0
        d2 = 0
        for name, dim_size in zip(names, dim_sizes):
            d2 = d1 + dim_size
            if dim_size == 1:
                self.data[name.rstrip()] = data[d1, :]
            else:
                self.data[name.rstrip()] = data[d1:d2, :]
            d1 += dim_size