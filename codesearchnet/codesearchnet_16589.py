def _read_all_attribute_info(self):
        """Read all attribute properties, g, r, and z attributes"""

        num = copy.deepcopy(self._num_attrs)
        fname = copy.deepcopy(self.fname)
        out = fortran_cdf.inquire_all_attr(fname, num, len(fname))
        status = out[0]
        names = out[1].astype('U')
        scopes = out[2]
        max_gentries = out[3]
        max_rentries = out[4]
        max_zentries = out[5]
        attr_nums = out[6]

        global_attrs_info = {}
        var_attrs_info = {}
        if status == 0:
            for name, scope, gentry, rentry, zentry, num in zip(names, scopes, max_gentries,
                                                                max_rentries, max_zentries,
                                                                attr_nums):
                name = ''.join(name)
                name = name.rstrip()
                nug = {}
                nug['scope'] = scope
                nug['max_gentry'] = gentry
                nug['max_rentry'] = rentry
                nug['max_zentry'] = zentry
                nug['attr_num'] = num
                flag = (gentry == 0) & (rentry == 0) & (zentry == 0)
                if not flag:
                    if scope == 1:
                        global_attrs_info[name] = nug
                    elif scope == 2:
                        var_attrs_info[name] = nug

            self.global_attrs_info = global_attrs_info
            self.var_attrs_info = var_attrs_info
        else:
            raise IOError(fortran_cdf.statusreporter(status))