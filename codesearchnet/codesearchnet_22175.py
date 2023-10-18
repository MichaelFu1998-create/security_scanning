def descendents(self):
        """Returns a list of descendents of this node."""
        visited = set([])
        self._depth_descend(self, visited)
        try:
            visited.remove(self)
        except KeyError:
            # we weren't descendent of ourself, that's ok
            pass

        return list(visited)