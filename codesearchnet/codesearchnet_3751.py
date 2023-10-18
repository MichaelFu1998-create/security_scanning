def associate_success_node(self, parent, child=None, **kwargs):
        """Add a node to run on success.

        =====API DOCS=====
        Add a node to run on success.

        :param parent: Primary key of parent node to associate success node to.
        :type parent: int
        :param child: Primary key of child node to be associated.
        :type child: int
        :param `**kwargs`: Fields used to create child node if ``child`` is not provided.
        :returns: Dictionary of only one key "changed", which indicates whether the association succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._assoc_or_create('success', parent, child, **kwargs)