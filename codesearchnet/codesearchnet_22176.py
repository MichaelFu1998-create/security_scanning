def descendents_root(self):
        """Returns a list of descendents of this node, if the root node is in
        the list (due to a cycle) it will be included but will not pass
        through it.  
        """
        visited = set([])
        self._depth_descend(self, visited, True)
        try:
            visited.remove(self)
        except KeyError:
            # we weren't descendent of ourself, that's ok
            pass

        return list(visited)