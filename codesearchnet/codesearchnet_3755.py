def associate_always_node(self, parent, child=None, **kwargs):
        """Add a node to always run after the parent is finished.

        =====API DOCS=====
        Add a node to always run after the parent is finished.

        :param parent: Primary key of parent node to associate always node to.
        :type parent: int
        :param child: Primary key of child node to be associated.
        :type child: int
        :param `**kwargs`: Fields used to create child node if ``child`` is not provided.
        :returns: Dictionary of only one key "changed", which indicates whether the association succeeded.
        :rtype: dict

        =====API DOCS=====
        """
        return self._assoc_or_create('always', parent, child, **kwargs)