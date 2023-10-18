def disassociate_success_node(self, parent, child):
        """Remove success node.
        The resulatant 2 nodes will both become root nodes.

        =====API DOCS=====
        Remove success node.

        :param parent: Primary key of parent node to disassociate success node from.
        :type parent: int
        :param child: Primary key of child node to be disassociated.
        :type child: int
        :returns: Dictionary of only one key "changed", which indicates whether the disassociation succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._disassoc(
            self._forward_rel_name('success'), parent, child)