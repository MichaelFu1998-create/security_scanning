def set_sim_params(self, nparams, attr_params):
        """Store parameters in `params` in `h5file.root.parameters`.

        `nparams` (dict)
            A dict as returned by `get_params()` in `ParticlesSimulation()`
            The format is:
            keys:
                used as parameter name
            values: (2-elements tuple)
                first element is the parameter value
                second element is a string used as "title" (description)
        `attr_params` (dict)
            A dict whole items are stored as attributes in '/parameters'
        """
        for name, value in nparams.items():
            val = value[0] if value[0] is not None else 'none'
            self.h5file.create_array('/parameters', name, obj=val,
                                     title=value[1])
        for name, value in attr_params.items():
            self.h5file.set_node_attr('/parameters', name, value)