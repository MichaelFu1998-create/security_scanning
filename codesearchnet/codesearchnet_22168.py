def factory(cls, data_class, **kwargs):
        """Creates a ``DCCGraph``, a root :class:`Node`: and the node's
        associated data class instance.  This factory is used to get around
        the chicken-and-egg problem of the ``DCCGraph`` and ``Nodes`` within
        it having pointers to each other.

        :param data_class: 
            django model class that extends :class:`BaseNodeData` and is used
            to associate information with the nodes in this graph
        :param kwargs: 
            arguments to pass to constructor of the data class instance that
            is to be created for the root node
        :returns: 
            instance of the newly created ``DCCGraph``
        """
        if not issubclass(data_class, BaseNodeData):
            raise AttributeError('data_class must be a BaseNodeData extender')

        content_type = ContentType.objects.get_for_model(data_class)
        graph = DCCGraph.objects.create(data_content_type=content_type)
        node = Node.objects.create(graph=graph)
        data_class.objects.create(node=node, **kwargs)
        graph.root = node
        graph.save()
        return graph