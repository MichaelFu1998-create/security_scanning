def get_file_name(self, f_term):
        """Returns first found fileName property or None if not found."""
        for _, _, name in self.graph.triples((f_term, self.spdx_namespace['fileName'], None)):
            return name
        return