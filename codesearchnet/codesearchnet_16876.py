def get_group_tabs(self):
        """
        Return instances of all other tabs that are members of the tab's
        tab group.
        """
        if self.tab_group is None:
            raise ImproperlyConfigured(
                "%s requires a definition of 'tab_group'" %
                self.__class__.__name__)
        group_members = [t for t in self._registry if t.tab_group == self.tab_group]
        return [t() for t in group_members]