def remove(self):
        """Removes the node from the graph.  Note this does not remove the
        associated data object.  See :func:`Node.can_remove` for limitations
        on what can be deleted.

        :returns: 
            :class:`BaseNodeData` subclass associated with the deleted Node

        :raises AttributeError:
           if called on a ``Node`` that cannot be deleted
        """
        if not self.can_remove():
            raise AttributeError('this node cannot be deleted')

        data = self.data
        self.parents.remove(self)
        self.delete()
        return data