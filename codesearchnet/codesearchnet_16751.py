def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""
        Impl.restore_state(self, system)
        BaseSpaceContainerImpl.restore_state(self, system)
        mapping = {}
        for node in self.cellgraph:
            if isinstance(node, tuple):
                name, key = node
            else:
                name, key = node, None
            cells = self.get_object(name)
            mapping[node] = get_node(cells, key, None)

        self.cellgraph = nx.relabel_nodes(self.cellgraph, mapping)