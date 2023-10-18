def factory_from_graph(cls, data_class, root_args, children):
        """Creates a ``DCCGraph`` and corresponding nodes.  The root_args parm
        is a dictionary specifying the parameters for creating a :class:`Node`
        and its corresponding :class:`BaseNodeData` subclass from the
        data_class specified.  The children parm is an iterable containing
        pairs of dictionaries and iterables, where the dictionaries specify
        the parameters for a :class:`BaseNodeData` subclass and the iterable
        the list of children.

        Example::

            DCCGraph.factory_from_graph(Label, 
                {'name':'A'}, [
                    ({'name':'B', []),
                    ({'name':'C', [])
                ])

        creates the graph::

                 A
                / \
               B   C

        :param data_class: 
            django model class that extends :class:`BaseNodeData` and is used
            to associate information with the Nodes in this graph
        :param root_args: 
            dictionary of arguments to pass to constructor of the data class
            instance that is to be created for the root node
        :param children: 
            iterable with a list of dictionary and iterable pairs
        :returns: 
            instance of the newly created ``DCCGraph``
        """
        graph = cls.factory(data_class, **root_args)
        for child in children:
            cls._depth_create(graph.root, child[0], child[1])

        return graph