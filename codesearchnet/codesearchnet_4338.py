def p_file_depends(self, f_term, predicate):
        """Sets file dependencies."""
        for _, _, other_file in self.graph.triples((f_term, predicate, None)):
            name = self.get_file_name(other_file)
            if name is not None:
                self.builder.add_file_dep(six.text_type(name))
            else:
                self.error = True
                msg = 'File depends on file with no name'
                self.logger.log(msg)