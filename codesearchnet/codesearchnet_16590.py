def _read_all_z_attribute_data(self):
        """Read all CDF z-attribute data"""
        self.meta = {}
        # collect attribute info needed to get more info from 
        # fortran routines
        max_entries = []
        attr_nums = []
        names = []
        attr_names = []
        names = self.var_attrs_info.keys()
        num_z_attrs = len(names)
        exp_attr_nums = []
        for key in names:
            max_entries.append(self.var_attrs_info[key]['max_zentry'])
            attr_nums.append(self.var_attrs_info[key]['attr_num'])
        attr_nums = np.array(attr_nums)
        max_entries = np.array(max_entries)

        info = fortran_cdf.z_attr_all_inquire(self.fname, attr_nums,
                                              num_z_attrs, max_entries, 
                                              self._num_z_vars, len(self.fname))

        status = info[0]
        data_types = info[1]
        num_elems = info[2]
        entry_nums = info[3]

        if status == 0:
            for i, name in enumerate(names):
                self.var_attrs_info[name]['data_type'] = data_types[i]
                self.var_attrs_info[name]['num_elems'] = num_elems[i]
                self.var_attrs_info[name]['entry_num'] = entry_nums[i]
                exp_attr_nums.extend([self.var_attrs_info[name]['attr_num']] * len(entry_nums[i]))
                attr_names.extend([name] * len(entry_nums[i]))
        else:
            raise IOError(fortran_cdf.statusreporter(status))

        # all the info is now packed up
        # need to break it out to make it easier to load via fortran
        # all of this junk
        # attribute  id, entry id (zVariable ID), data_type, num_elems
        # should just need to flatten this stuff

        data_types = data_types.flatten()
        num_elems = num_elems.flatten()
        entry_nums = entry_nums.flatten()
        attr_nums = np.array(exp_attr_nums)
        # drop everything that isn't valid
        idx, = np.where(entry_nums > 0)

        data_types = data_types[idx]
        num_elems = num_elems[idx]
        entry_nums = entry_nums[idx]
        attr_nums = attr_nums[idx]
        attr_names = np.array(attr_names)[idx]
        # grad corresponding variable name for each attribute
        var_names = [self.z_variable_names_by_num[i].rstrip() for i in entry_nums]

        # the names that go along with this are already set up

        # in attr_names
        # chunk by data type, grab largest num_elems

        # get data back, shorten to num_elems, add to structure
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['real4'],
                                        fortran_cdf.get_multi_z_attr_real4)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['float'],
                                        fortran_cdf.get_multi_z_attr_real4)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['real8'],
                                        fortran_cdf.get_multi_z_attr_real8)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['double'],
                                        fortran_cdf.get_multi_z_attr_real8)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['byte'],
                                        fortran_cdf.get_multi_z_attr_int1)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['int1'],
                                        fortran_cdf.get_multi_z_attr_int1)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['uint1'],
                                        fortran_cdf.get_multi_z_attr_int1,
                                        data_offset=256)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['int2'],
                                        fortran_cdf.get_multi_z_attr_int2)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['uint2'],
                                        fortran_cdf.get_multi_z_attr_int2,
                                        data_offset=65536)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['int4'],
                                        fortran_cdf.get_multi_z_attr_int4)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['uint4'],
                                        fortran_cdf.get_multi_z_attr_int4,
                                        data_offset=2 ** 32)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['char'],
                                        fortran_cdf.get_multi_z_attr_char)
        self._call_multi_fortran_z_attr(attr_names, data_types, num_elems,
                                        entry_nums, attr_nums, var_names, self.cdf_data_types['uchar'],
                                        fortran_cdf.get_multi_z_attr_char)