def add_namespace_to_graph(self, graph: BELGraph) -> Namespace:
        """Add this manager's namespace to the graph."""
        namespace = self.upload_bel_namespace()
        graph.namespace_url[namespace.keyword] = namespace.url

        # Add this manager as an annotation, too
        self._add_annotation_to_graph(graph)

        return namespace