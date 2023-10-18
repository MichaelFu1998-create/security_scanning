def _new_dynspace(
        self,
        name=None,
        bases=None,
        formula=None,
        refs=None,
        arguments=None,
        source=None,
    ):
        """Create a new dynamic root space."""

        if name is None:
            name = self.spacenamer.get_next(self.namespace)

        if name in self.namespace:
            raise ValueError("Name '%s' already exists." % name)

        if not is_valid_name(name):
            raise ValueError("Invalid name '%s'." % name)

        space = RootDynamicSpaceImpl(
            parent=self,
            name=name,
            formula=formula,
            refs=refs,
            source=source,
            arguments=arguments,
        )
        space.is_derived = False
        self._set_space(space)

        if bases:  # i.e. not []
            dynbase = self._get_dynamic_base(bases)
            space._dynbase = dynbase
            dynbase._dynamic_subs.append(space)

        return space