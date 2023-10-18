def ancestors_root(self):
        """Returns a list of the ancestors of this node but does not pass the
        root node, even if the root has parents due to cycles."""
        if self.is_root():
            return []

        ancestors = set([])
        self._depth_ascend(self, ancestors, True)
        try:
            ancestors.remove(self)
        except KeyError:
            # we weren't ancestor of ourself, that's ok
            pass

        return list(ancestors)