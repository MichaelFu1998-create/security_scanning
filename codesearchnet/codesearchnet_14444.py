def _create_kernel(self):
        """
        creates an additive kernel
        """
        # Check kernels
        kernels = self.kernel_params
        if not isinstance(kernels, list):
            raise RuntimeError('Must provide enumeration of kernels')
        for kernel in kernels:
            if sorted(list(kernel.keys())) != ['name', 'options', 'params']:
                raise RuntimeError(
                    'strategy/params/kernels must contain keys: "name", "options", "params"')

        # Turn into entry points.
        # TODO use eval to allow user to specify internal variables for kernels (e.g. V) in config file.
        kernels = []
        for kern in self.kernel_params:
            params = kern['params']
            options = kern['options']
            name = kern['name']
            kernel_ep = load_entry_point(name, 'strategy/params/kernels')
            if issubclass(kernel_ep, KERNEL_BASE_CLASS):
                if options['independent']:
                    # TODO Catch errors here?  Estimator entry points don't catch instantiation errors
                    kernel = np.sum([kernel_ep(1, active_dims=[i], **params) for i in range(self.n_dims)])
                else:
                    kernel = kernel_ep(self.n_dims, **params)
            if not isinstance(kernel, KERNEL_BASE_CLASS):
                raise RuntimeError('strategy/params/kernel must load a'
                                   'GPy derived Kernel')
            kernels.append(kernel)

        self.kernel = np.sum(kernels)