def get_review_date(self, r_term):
        """Returns review date or None if not found.
        Reports error on failure.
        Note does not check value format.
        """
        reviewed_list = list(self.graph.triples((r_term, self.spdx_namespace['reviewDate'], None)))
        if len(reviewed_list) != 1:
            self.error = True
            msg = 'Review must have exactlyone review date'
            self.logger.log(msg)
            return
        return six.text_type(reviewed_list[0][2])