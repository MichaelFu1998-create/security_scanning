def p_file_cr_text(self, f_term, predicate):
        """Sets file copyright text."""
        try:
            for _, _, cr_text in self.graph.triples((f_term, predicate, None)):
                self.builder.set_file_copyright(self.doc, six.text_type(cr_text))
        except CardinalityError:
            self.more_than_one_error('file copyright text')