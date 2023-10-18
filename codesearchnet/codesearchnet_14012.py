def nodes_by_category(self, category):
        """ Returns nodes with the given category attribute.
        """
        return [n for n in self.nodes if n.category == category]