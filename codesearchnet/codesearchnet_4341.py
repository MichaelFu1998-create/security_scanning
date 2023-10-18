def p_file_comment(self, f_term, predicate):
        """Sets file comment text."""
        try:
            for _, _, comment in self.graph.triples((f_term, predicate, None)):
                self.builder.set_file_comment(self.doc, six.text_type(comment))
        except CardinalityError:
            self.more_than_one_error('file comment')