def get_annotation_date(self, r_term):
        """Returns annotation date or None if not found.
        Reports error on failure.
        Note does not check value format.
        """
        annotation_date_list = list(self.graph.triples((r_term, self.spdx_namespace['annotationDate'], None)))
        if len(annotation_date_list) != 1:
            self.error = True
            msg = 'Annotation must have exactly one annotation date.'
            self.logger.log(msg)
            return
        return six.text_type(annotation_date_list[0][2])