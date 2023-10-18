def to_indra_statements(self, *args, **kwargs):
        """Dump as a list of INDRA statements.

        :rtype: List[indra.Statement]
        """
        graph = self.to_bel(*args, **kwargs)
        return to_indra_statements(graph)