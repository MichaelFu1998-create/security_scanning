def get_extr_lics_comment(self, extr_lics):
        """
        Return license comment or None.
        """
        comment_list = list(self.graph.triples(
            (extr_lics, RDFS.comment, None)))
        if len(comment_list) > 1 :
            self.more_than_one_error('extracted license comment')
            return
        elif len(comment_list) == 1:
            return comment_list[0][2]
        else:
            return