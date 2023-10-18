def p_file_comments_on_lics(self, f_term, predicate):
        """Sets file license comment."""
        try:
            for _, _, comment in self.graph.triples((f_term, predicate, None)):
                self.builder.set_file_license_comment(self.doc, six.text_type(comment))
        except CardinalityError:
            self.more_than_one_error('file comments on license')