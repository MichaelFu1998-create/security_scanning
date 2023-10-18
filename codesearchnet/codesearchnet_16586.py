def load_all_variables(self):
        """Loads all variables from CDF.
        
        Note this routine is called automatically
        upon instantiation.
        
        """

        self.data = {}
        # need to add r variable names
        file_var_names = self.z_variable_info.keys()
        # collect variable information for each
        # organize it neatly for fortran call
        dim_sizes = []
        rec_nums = []
        data_types = []
        names = []
        for i, name in enumerate(file_var_names):
            dim_sizes.extend(self.z_variable_info[name]['dim_sizes'])
            rec_nums.append(self.z_variable_info[name]['rec_num'])
            data_types.append(self.z_variable_info[name]['data_type'])
            names.append(name.ljust(256))
        dim_sizes = np.array(dim_sizes)
        rec_nums = np.array(rec_nums)
        data_types = np.array(data_types)
        # individually load all variables by each data type
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['real4'],
                                   fortran_cdf.get_multi_z_real4)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['float'],
                                   fortran_cdf.get_multi_z_real4)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['real8'],
                                   fortran_cdf.get_multi_z_real8)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['double'],
                                   fortran_cdf.get_multi_z_real8)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['int4'],
                                   fortran_cdf.get_multi_z_int4)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['uint4'],
                                   fortran_cdf.get_multi_z_int4,
                                   data_offset=2 ** 32)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['int2'],
                                   fortran_cdf.get_multi_z_int2)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['uint2'],
                                   fortran_cdf.get_multi_z_int2,
                                   data_offset=2 ** 16)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['int1'],
                                   fortran_cdf.get_multi_z_int1)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['uint1'],
                                   fortran_cdf.get_multi_z_int1,
                                   data_offset=2 ** 8)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['byte'],
                                   fortran_cdf.get_multi_z_int1)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['epoch'],
                                   fortran_cdf.get_multi_z_real8,
                                   epoch=True)
        self._call_multi_fortran_z(names, data_types, rec_nums, 2 * dim_sizes,
                                   self.cdf_data_types['epoch16'],
                                   fortran_cdf.get_multi_z_epoch16,
                                   epoch16=True)
        self._call_multi_fortran_z(names, data_types, rec_nums, dim_sizes,
                                   self.cdf_data_types['TT2000'],
                                   fortran_cdf.get_multi_z_tt2000,
                                   epoch=True)
        # mark data has been loaded
        self.data_loaded = True