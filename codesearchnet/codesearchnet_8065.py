def get_params(self, deep=True):
        '''Get the parameters for this object.  Returns as a dict.

        Parameters
        ----------
        deep : bool
            Recurse on nested objects

        Returns
        -------
        params : dict
            A dictionary containing all parameters for this object
        '''

        out = dict(__class__=self.__class__,
                   params=dict())

        for key in self._get_param_names():
            value = getattr(self, key, None)

            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out['params'][key] = dict(__class__=value.__class__)
                out['params'][key].update((k, val) for k, val in deep_items)
            else:
                out['params'][key] = value

        return out