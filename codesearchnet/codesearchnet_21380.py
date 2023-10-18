def remove_tag(self, tag):
        """
            Removes a tag from this object
        """
        self.tags = list(set(self.tags or []) - set([tag]))