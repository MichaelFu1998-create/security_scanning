def disassociate_always_node(self, parent, child):
        """Remove an always node link.
        The resultant 2 nodes will both become root nodes.

        =====API DOCS=====
        Remove an always node link.

        :param parent: Primary key of parent node to disassociate always node from.
        :type parent: int
        :param child: Primary key of child node to be disassociated.
        :type child: int
        :returns: Dictionary of only one key "changed", which indicates whether the disassociation succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._disassoc(
            self._forward_rel_name('always'), parent, child)