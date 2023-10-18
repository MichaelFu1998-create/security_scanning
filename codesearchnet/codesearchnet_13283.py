def groups(self):
        """Set of groups defined in the roster.

        :Return: the groups
        :ReturnType: `set` of `unicode`
        """
        groups = set()
        for item in self._items:
            groups |= item.groups
        return groups