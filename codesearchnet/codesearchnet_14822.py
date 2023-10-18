def _pop(self, model):
        """Pop all matching tags off the model and return them."""
        tags = []

        # collect any exsiting tags with matching prefix
        for tag in model.tags:
            if self.is_tag(tag):
                tags.append(tag)

        # remove collected tags from model
        if tags:
            for tag in tags:
                model.tags.remove(tag)

        return tags