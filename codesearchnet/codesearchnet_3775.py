def associate(self, group, parent, **kwargs):
        """Associate this group with the specified group.

        =====API DOCS=====
        Associate this group with the specified group.

        :param group: Primary key or name of the child group to associate.
        :type group: str
        :param parent: Primary key or name of the parent group to associate to.
        :type parent: str
        :param inventory: Primary key or name of the inventory the association should happen in.
        :type inventory: str
        :returns: Dictionary of only one key "changed", which indicates whether the association succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        parent_id = self.lookup_with_inventory(parent, kwargs.get('inventory', None))['id']
        group_id = self.lookup_with_inventory(group, kwargs.get('inventory', None))['id']
        return self._assoc('children', parent_id, group_id)