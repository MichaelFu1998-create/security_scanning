def ancestors(self):
        """Returns a list of the ancestors of this node."""
        ancestors = set([])
        self._depth_ascend(self, ancestors)
        try:
            ancestors.remove(self)
        except KeyError:
            # we weren't ancestor of ourself, that's ok
            pass

        return list(ancestors)