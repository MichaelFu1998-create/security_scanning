def can_remove(self):
        """Returns True if it is legal to remove this node and still leave the
        graph as a single connected entity, not splitting it into a forest.
        Only nodes with no children or those who cause a cycle can be deleted.
        """
        if self.children.count() == 0:
            return True

        ancestors = set(self.ancestors_root())
        children = set(self.children.all())
        return children.issubset(ancestors)