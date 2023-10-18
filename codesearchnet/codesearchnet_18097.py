def set_values(self, params, values):
        """
        Directly set the values corresponding to certain parameters.
        This does not necessarily trigger and update of the calculation,
        
        See also
        --------
        :func:`~peri.comp.comp.ParameterGroup.update` : full update func
        """
        for p, v in zip(util.listify(params), util.listify(values)):
            self.param_dict[p] = v