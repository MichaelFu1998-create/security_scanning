def _citation_processor(self, retrieved):
        """ Return a list of strings formatted as HTML citation entries
        """
        items = []
        for cit in retrieved.entries:
            items.append(cit["content"][0]["value"])
        self.url_params = None
        return items