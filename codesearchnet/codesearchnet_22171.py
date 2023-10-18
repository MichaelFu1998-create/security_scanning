def add_child(self, **kwargs):
        """Creates a new ``Node`` based on the extending class and adds it as
        a child to this ``Node``.

        :param kwargs: 
            arguments for constructing the data object associated with this
            ``Node``
        :returns: 
            extender of the ``Node`` class
        """
        data_class = self.graph.data_content_type.model_class()
        node = Node.objects.create(graph=self.graph)
        data_class.objects.create(node=node, **kwargs)
        node.parents.add(self)
        self.children.add(node)
        return node