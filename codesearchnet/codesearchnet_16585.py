def _read_all_z_variable_info(self):
        """Gets all CDF z-variable information, not data though.

        Maps to calls using var_inquire. Gets information on
        data type, number of elements, number of dimensions, etc.

        """

        self.z_variable_info = {}
        self.z_variable_names_by_num = {}

        # call Fortran that grabs all of the basic stats on all of the
        # zVariables in one go.
        info = fortran_cdf.z_var_all_inquire(self.fname, self._num_z_vars,
                                             len(self.fname))
        status = info[0]
        data_types = info[1]
        num_elems = info[2]
        rec_varys = info[3]
        dim_varys = info[4]
        num_dims = info[5]
        dim_sizes = info[6]
        rec_nums = info[7]
        var_nums = info[8]
        var_names = info[9]

        if status == 0:
            for i in np.arange(len(data_types)):
                out = {}
                out['data_type'] = data_types[i]
                out['num_elems'] = num_elems[i]
                out['rec_vary'] = rec_varys[i]
                out['dim_varys'] = dim_varys[i]
                out['num_dims'] = num_dims[i]
                # only looking at first possible extra dimension
                out['dim_sizes'] = dim_sizes[i, :1]
                if out['dim_sizes'][0] == 0:
                    out['dim_sizes'][0] += 1
                out['rec_num'] = rec_nums[i]
                out['var_num'] = var_nums[i]
                var_name = ''.join(var_names[i].astype('U'))
                out['var_name'] = var_name.rstrip()
                self.z_variable_info[out['var_name']] = out
                self.z_variable_names_by_num[out['var_num']] = var_name
        else:
            raise IOError(fortran_cdf.statusreporter(status))