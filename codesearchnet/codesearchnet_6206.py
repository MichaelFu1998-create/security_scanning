def _replace_on_id(self, new_object):
        """Replace an object by another with the same id."""
        the_id = new_object.id
        the_index = self._dict[the_id]
        list.__setitem__(self, the_index, new_object)