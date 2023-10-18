def add_members(self, new_members):
        """
        Add objects to the group.

        Parameters
        ----------
        new_members : list
            A list of cobrapy objects to add to the group.

        """

        if isinstance(new_members, string_types) or \
                hasattr(new_members, "id"):
            warn("need to pass in a list")
            new_members = [new_members]

        self._members.update(new_members)