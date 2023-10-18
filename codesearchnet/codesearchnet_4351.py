def get_reviewer(self, r_term):
        """Returns reviewer as creator object or None if failed.
        Reports errors on failure.
        """
        reviewer_list = list(self.graph.triples((r_term, self.spdx_namespace['reviewer'], None)))
        if len(reviewer_list) != 1:
            self.error = True
            msg = 'Review must have exactly one reviewer'
            self.logger.log(msg)
            return
        try:
            return self.builder.create_entity(self.doc, six.text_type(reviewer_list[0][2]))
        except SPDXValueError:
            self.value_error('REVIEWER_VALUE', reviewer_list[0][2])