def p_file_contributor(self, f_term, predicate):
        """
        Parse all file contributors and adds them to the model.
        """
        for _, _, contributor in self.graph.triples((f_term, predicate, None)):
            self.builder.add_file_contribution(self.doc, six.text_type(contributor))