def p_file_notice(self, f_term, predicate):
        """Sets file notice text."""
        try:
            for _, _, notice in self.graph.triples((f_term, predicate, None)):
                self.builder.set_file_notice(self.doc, six.text_type(notice))
        except CardinalityError:
            self.more_than_one_error('file notice')