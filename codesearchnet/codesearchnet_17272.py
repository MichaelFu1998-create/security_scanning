def in_out_ratio(self, node: BaseEntity) -> float:
        """Calculate the ratio of in-degree / out-degree of a node."""
        return self.graph.in_degree(node) / float(self.graph.out_degree(node))