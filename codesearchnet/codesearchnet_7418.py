def add_tags(self, item, *tags):
        """
        Add one or more tags to a retrieved item,
        then update it on the server
        Accepts a dict, and one or more tags to add to it
        Returns the updated item from the server
        """
        # Make sure there's a tags field, or add one
        try:
            assert item["data"]["tags"]
        except AssertionError:
            item["data"]["tags"] = list()
        for tag in tags:
            item["data"]["tags"].append({"tag": "%s" % tag})
        # make sure everything's OK
        assert self.check_items([item])
        return self.update_item(item)