def get_annotation_type(self, r_term):
        """Returns annotation type or None if found none or more than one.
        Reports errors on failure."""
        for _, _, typ in self.graph.triples((
                r_term, self.spdx_namespace['annotationType'], None)):
            if typ is not None:
                return typ
            else:
                self.error = True
                msg = 'Annotation must have exactly one annotation type.'
                self.logger.log(msg)
                return