def set(self, target, value):
        """Set the value of this attribute for the passed object.
        """

        if not self._set:
            return

        if self.path is None:
            # There is no path defined on this resource.
            # We can do no magic to set the value.
            self.set = lambda *a: None
            return None

        if self._segments[target.__class__]:
            # Attempt to resolve access to this attribute.
            self.get(target)

        if self._segments[target.__class__]:
            # Attribute is not fully resolved; an interim segment is null.
            return

        # Resolve access to the parent object.
        # For a single-segment path this will effectively be a no-op.
        parent_getter = compose(*self._getters[target.__class__][:-1])
        target = parent_getter(target)

        # Make the setter.
        func = self._make_setter(self.path.split('.')[-1], target.__class__)

        # Apply the setter now.
        func(target, value)

        # Replace this function with the constructed setter.
        def setter(target, value):
            func(parent_getter(target), value)

        self.set = setter