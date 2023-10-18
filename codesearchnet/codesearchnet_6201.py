def remove_members(self, to_remove):
        """
        Remove objects from the group.

        Parameters
        ----------
        to_remove : list
            A list of cobra objects to remove from the group
        """

        if isinstance(to_remove, string_types) or \
                hasattr(to_remove, "id"):
            warn("need to pass in a list")
            to_remove = [to_remove]

        self._members.difference_update(to_remove)