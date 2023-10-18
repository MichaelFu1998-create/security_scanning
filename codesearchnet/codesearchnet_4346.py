def p_file_lic_info(self, f_term, predicate):
        """Sets file license information."""
        for _, _, info in self.graph.triples((f_term, predicate, None)):
            lic = self.handle_lics(info)
            if lic is not None:
                self.builder.set_file_license_in_file(self.doc, lic)