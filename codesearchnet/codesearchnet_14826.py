def get_all(self, model):
        """Get all known tags from a model.

        Returns a dict of {<tag_name>:<tag_value>}.
        """
        tags = {}
        for name, tag in self.tags.items():
            for mtag in model.tags:
                if tag.is_tag(mtag):
                    tags[name] = tag.get(model)
        return tags