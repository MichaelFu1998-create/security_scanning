def _process_return_multi_z_attr(self, data, attr_names, var_names, sub_num_elems):
        '''process and attach data from fortran_cdf.get_multi_*'''
        # process data

        for i, (attr_name, var_name, num_e) in enumerate(zip(attr_names, var_names, sub_num_elems)):
            if var_name not in self.meta.keys():
                self.meta[var_name] = {}
            if num_e == 1:
                self.meta[var_name][attr_name] = data[i, 0]
            else:
                if data[i].dtype == '|S1':
                    self.meta[var_name][attr_name] = ''.join(data[i, 0:num_e].astype('U')).rstrip()
                else:
                    self.meta[var_name][attr_name] = data[i, 0:num_e]