def _get_init_args(self, skip=4):
        """Get all arguments of current layer for saving the graph."""
        stack = inspect.stack()

        if len(stack) < skip + 1:
            raise ValueError("The length of the inspection stack is shorter than the requested start position.")

        args, _, _, values = inspect.getargvalues(stack[skip][0])

        params = {}

        for arg in args:

            # some args dont need to be saved into the graph. e.g. the input placeholder
            if values[arg] is not None and arg not in ['self', 'prev_layer', 'inputs']:

                val = values[arg]

                # change function (e.g. act) into dictionary of module path and function name
                if inspect.isfunction(val):
                    params[arg] = {"module_path": val.__module__, "func_name": val.__name__}
                # ignore more args e.g. TF class
                elif arg.endswith('init'):
                    continue
                # for other data type, save them directly
                else:
                    params[arg] = val

        return params