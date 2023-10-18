def get_values(self, params):
        """
        Get the value of a list or single parameter.

        Parameters
        ----------
        params : string, list of string
            name of parameters which to retrieve
        """
        return util.delistify(
            [self.param_dict[p] for p in util.listify(params)], params
        )