def count_relations(self) -> int:
        """Count the number of BEL relations generated."""
        if self.edge_model is ...:
            raise Bio2BELMissingEdgeModelError('edge_edge model is undefined/count_bel_relations is not overridden')
        elif isinstance(self.edge_model, list):
            return sum(self._count_model(m) for m in self.edge_model)
        else:
            return self._count_model(self.edge_model)