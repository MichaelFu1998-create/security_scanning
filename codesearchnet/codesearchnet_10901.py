def add_trajectory(self, name, overwrite=False, shape=(0,), title='',
                       chunksize=2**19, comp_filter=default_compression,
                       atom=tables.Float64Atom(), params=dict(),
                       chunkslice='bytes'):
        """Add an trajectory array in '/trajectories'.
        """
        group = self.h5file.root.trajectories
        if name in group:
            print("%s already exists ..." % name, end='')
            if overwrite:
                self.h5file.remove_node(group, name)
                print(" deleted.")
            else:
                print(" old returned.")
                return group.get_node(name)

        nparams = self.numeric_params
        num_t_steps = nparams['t_max'] / nparams['t_step']

        chunkshape = self.calc_chunkshape(chunksize, shape, kind=chunkslice)
        store_array = self.h5file.create_earray(
            group, name, atom=atom,
            shape = shape,
            chunkshape = chunkshape,
            expectedrows = num_t_steps,
            filters = comp_filter,
            title = title)

        # Set the array parameters/attributes
        for key, value in params.items():
            store_array.set_attr(key, value)
        store_array.set_attr('PyBroMo', __version__)
        store_array.set_attr('creation_time', current_time())
        return store_array