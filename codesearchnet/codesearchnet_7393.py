def num_tagitems(self, tag):
        """ Return the total number of items for the specified tag
        """
        query = "/{t}/{u}/tags/{ta}/items".format(
            u=self.library_id, t=self.library_type, ta=tag
        )
        return self._totals(query)