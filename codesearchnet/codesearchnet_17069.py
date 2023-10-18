def insert_graph(self, graph: BELGraph, **_kwargs) -> Network:
        """Insert a graph and return the resulting ORM object (mocked)."""
        result = _Namespace()
        result.id = len(self.networks)

        self.networks[result.id] = graph

        return result