def _call_multi_fortran_z(self, names, data_types, rec_nums,
                              dim_sizes, input_type_code, func,
                              epoch=False, data_offset=None, epoch16=False):
        """Calls fortran functions to load CDF variable data

        Parameters
        ----------
        names : list_like
            list of variables names
        data_types : list_like
            list of all loaded data type codes as used by CDF
        rec_nums : list_like
            list of record numbers in CDF file. Provided by variable_info
        dim_sizes :
            list of dimensions as provided by variable_info.
        input_type_code : int
            Specific type code to load
        func : function
            Fortran function via python interface that will be used for actual loading.
        epoch : bool
            Flag indicating type is epoch. Translates things to datetime standard.
        data_offset :
            Offset value to be applied to data. Required for unsigned integers in CDF.
        epoch16 : bool
            Flag indicating type is epoch16. Translates things to datetime standard.

        
        """

        # isolate input type code variables from total supplied types
        idx, = np.where(data_types == input_type_code)

        if len(idx) > 0:
            # read all data of a given type at once
            max_rec = rec_nums[idx].max()
            sub_names = np.array(names)[idx]
            sub_sizes = dim_sizes[idx]
            status, data = func(self.fname, sub_names.tolist(),
                                sub_sizes, sub_sizes.sum(), max_rec, len(sub_names))
            if status == 0:
                # account for quirks of CDF data storage for certain types
                if data_offset is not None:
                    data = data.astype(int)
                    idx, idy, = np.where(data < 0)
                    data[idx, idy] += data_offset
                if epoch:
                    # account for difference in seconds between
                    # CDF epoch and python's epoch, leap year in there
                    # (datetime(1971,1,2) - 
                    #      datetime(1,1,1)).total_seconds()*1000
                    data -= 62167219200000
                    data = data.astype('<M8[ms]')
                if epoch16:
                    data[0::2, :] -= 62167219200
                    data = data[0::2, :] * 1E9 + data[1::2, :] / 1.E3
                    data = data.astype('datetime64[ns]')
                    sub_sizes /= 2
                # all data of a type has been loaded and tweaked as necessary
                # parse through returned array to break out the individual variables
                # as appropriate
                self._process_return_multi_z(data, sub_names, sub_sizes)
            else:
                raise IOError(fortran_cdf.statusreporter(status))