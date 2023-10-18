def get_object(self, name):
        """Retrieve an object by a dotted name relative to the space."""

        parts = name.split(".")
        child = parts.pop(0)

        if parts:
            return self.spaces[child].get_object(".".join(parts))
        else:
            return self._namespace_impl[child]