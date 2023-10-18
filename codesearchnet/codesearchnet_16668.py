def new_space_from_module(self, module, recursive=False, **params):
        """Create a child space from an module.

        Alias to :py:meth:`import_module`.

        Args:
            module: a module object or name of the module object.
            recursive: Not yet implemented.
            **params: arguments to pass to ``new_space``

        Returns:
            The new child space created from the module.
        """
        if "bases" in params:
            params["bases"] = get_impls(params["bases"])

        space = (
            self._impl.model.currentspace
        ) = self._impl.new_space_from_module(
            module, recursive=recursive, **params
        )
        return get_interfaces(space)