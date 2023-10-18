def get_annotation_comment(self, r_term):
        """Returns annotation comment or None if found none or more than one.
        Reports errors.
        """
        comment_list = list(self.graph.triples((r_term, RDFS.comment, None)))
        if len(comment_list) > 1:
            self.error = True
            msg = 'Annotation can have at most one comment.'
            self.logger.log(msg)
            return
        else:
            return six.text_type(comment_list[0][2])