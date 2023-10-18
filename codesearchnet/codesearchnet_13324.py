def prepare_query(self, data):
        """Complete string preparation procedure for 'query' strings.
        (without checks for unassigned codes)

        :Parameters:
            - `data`: Unicode string to prepare.

        :return: prepared string

        :raise StringprepError: if the preparation fails
        """
        data = self.map(data)
        if self.normalization:
            data = self.normalization(data)
        data = self.prohibit(data)
        if self.bidi:
            data = self.check_bidi(data)
        if isinstance(data, list):
            data = u"".join(data)
        return data