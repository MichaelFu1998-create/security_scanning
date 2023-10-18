def get_all_tags(self):
        """
            This method returns a list of all tags.
        """
        data = self.get_data("tags")
        return [
            Tag(token=self.token, **tag) for tag in data['tags']
        ]