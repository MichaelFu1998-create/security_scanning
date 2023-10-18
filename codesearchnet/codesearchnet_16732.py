def get_dynspace(self, args, kwargs=None):
        """Create a dynamic root space

        Called from interface methods
        """

        node = get_node(self, *convert_args(args, kwargs))
        key = node[KEY]

        if key in self.param_spaces:
            return self.param_spaces[key]

        else:
            last_self = self.system.self
            self.system.self = self

            try:
                space_args = self.eval_formula(node)

            finally:
                self.system.self = last_self

            if space_args is None:
                space_args = {"bases": [self]}  # Default
            else:
                if "bases" in space_args:
                    bases = get_impls(space_args["bases"])
                    if isinstance(bases, StaticSpaceImpl):
                        space_args["bases"] = [bases]
                    elif bases is None:
                        space_args["bases"] = [self]  # Default
                    else:
                        space_args["bases"] = bases
                else:
                    space_args["bases"] = [self]

            space_args["arguments"] = node_get_args(node)
            space = self._new_dynspace(**space_args)
            self.param_spaces[key] = space
            space.inherit(clear_value=False)
            return space