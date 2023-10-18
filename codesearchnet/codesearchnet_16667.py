def import_module(self, module=None, recursive=False, **params):
        """Create a child space from an module.

        Args:
            module: a module object or name of the module object.
            recursive: Not yet implemented.
            **params: arguments to pass to ``new_space``

        Returns:
            The new child space created from the module.
        """
        if module is None:
            if "module_" in params:
                warnings.warn(
                    "Parameter 'module_' is deprecated. Use 'module' instead.")
                module = params.pop("module_")
            else:
                raise ValueError("no module specified")

        if "bases" in params:
            params["bases"] = get_impls(params["bases"])

        space = (
            self._impl.model.currentspace
        ) = self._impl.new_space_from_module(
            module, recursive=recursive, **params
        )
        return get_interfaces(space)