def add_tag(self, tag):
        """
            Adds a tag to the list of tags and makes sure the result list contains only unique results.
        """
        self.tags = list(set(self.tags or []) | set([tag]))