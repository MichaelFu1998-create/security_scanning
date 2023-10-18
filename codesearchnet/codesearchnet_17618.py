def clone(self):
        """Create a complete copy of the stream.

        :returns: A new MaterialStream object."""

        result = copy.copy(self)
        result._compound_mfrs = copy.deepcopy(self._compound_mfrs)
        return result