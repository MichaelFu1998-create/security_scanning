def iter_leaves(self) -> Iterable[BaseEntity]:
        """Return an iterable over all nodes that are leaves.

        A node is a leaf if either:

         - it doesn't have any predecessors, OR
         - all of its predecessors have a score in their data dictionaries
        """
        for node in self.graph:
            if self.tag in self.graph.nodes[node]:
                continue

            if not any(self.tag not in self.graph.nodes[p] for p in self.graph.predecessors(node)):
                yield node