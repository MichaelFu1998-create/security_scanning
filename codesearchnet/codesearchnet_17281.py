def calculate_score(self, node: BaseEntity) -> float:
        """Calculate the new score of the given node."""
        score = (
            self.graph.nodes[node][self.tag]
            if self.tag in self.graph.nodes[node] else
            self.default_score
        )

        for predecessor, _, d in self.graph.in_edges(node, data=True):
            if d[RELATION] in CAUSAL_INCREASE_RELATIONS:
                score += self.graph.nodes[predecessor][self.tag]
            elif d[RELATION] in CAUSAL_DECREASE_RELATIONS:
                score -= self.graph.nodes[predecessor][self.tag]

        return score