def creators(self):
        """
        Return a list of creator nodes.
        Note: Does not add anything to the graph.
        """
        return map(lambda c: Literal(c.to_value()), self.document.creation_info.creators)