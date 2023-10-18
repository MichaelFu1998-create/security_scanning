def index(self, id, *args):
        """Determine the position in the list

        id: A string or a :class:`~cobra.core.Object.Object`

        """
        # because values are unique, start and stop are not relevant
        if isinstance(id, string_types):
            try:
                return self._dict[id]
            except KeyError:
                raise ValueError("%s not found" % id)
        try:
            i = self._dict[id.id]
            if self[i] is not id:
                raise ValueError(
                    "Another object with the identical id (%s) found" % id.id)
            return i
        except KeyError:
            raise ValueError("%s not found" % str(id))