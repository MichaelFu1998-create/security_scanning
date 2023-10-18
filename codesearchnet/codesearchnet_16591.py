def _call_multi_fortran_z_attr(self, names, data_types, num_elems,
                                   entry_nums, attr_nums, var_names,
                                   input_type_code, func, data_offset=None):
        """Calls Fortran function that reads attribute data.
        
        data_offset translates unsigned into signed.
        If number read in is negative, offset added.
        """
        # isolate input type code variables
        idx, = np.where(data_types == input_type_code)

        if len(idx) > 0:
            # maximimum array dimension
            max_num = num_elems[idx].max()
            sub_num_elems = num_elems[idx]
            sub_names = np.array(names)[idx]
            sub_var_names = np.array(var_names)[idx]
            # zVariable numbers, 'entry' number
            sub_entry_nums = entry_nums[idx]
            # attribute number
            sub_attr_nums = attr_nums[idx]
            status, data = func(self.fname, sub_attr_nums, sub_entry_nums,
                                len(sub_attr_nums), max_num, len(self.fname))
            if (status == 0).all():
                if data_offset is not None:
                    data = data.astype(int)
                    idx, idy, = np.where(data < 0)
                    data[idx, idy] += data_offset
                self._process_return_multi_z_attr(data, sub_names,
                                                  sub_var_names, sub_num_elems)
            else:
                # raise ValueError('CDF Error code :', status)
                idx, = np.where(status != 0)
                # raise first error
                raise IOError(fortran_cdf.statusreporter(status[idx][0]))