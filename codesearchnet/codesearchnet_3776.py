def disassociate(self, group, parent, **kwargs):
        """Disassociate this group from the specified group.

        =====API DOCS=====
        Disassociate this group with the specified group.

        :param group: Primary key or name of the child group to disassociate.
        :type group: str
        :param parent: Primary key or name of the parent group to disassociate from.
        :type parent: str
        :param inventory: Primary key or name of the inventory the disassociation should happen in.
        :type inventory: str
        :returns: Dictionary of only one key "changed", which indicates whether the disassociation succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        parent_id = self.lookup_with_inventory(parent, kwargs.get('inventory', None))['id']
        group_id = self.lookup_with_inventory(group, kwargs.get('inventory', None))['id']
        return self._disassoc('children', parent_id, group_id)