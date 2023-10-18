def _add_annotation_to_graph(self, graph: BELGraph) -> None:
        """Add this manager as an annotation to the graph."""
        if 'bio2bel' not in graph.annotation_list:
            graph.annotation_list['bio2bel'] = set()

        graph.annotation_list['bio2bel'].add(self.module_name)