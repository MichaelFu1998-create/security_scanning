def unscored_nodes_iter(self) -> BaseEntity:
        """Iterate over all nodes without a score."""
        for node, data in self.graph.nodes(data=True):
            if self.tag not in data:
                yield node