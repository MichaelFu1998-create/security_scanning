def get(self, model):
        """Get a matching valid tag off the model."""
        for tag in model.tags:
            if self.is_tag(tag):
                value = self.deserialize(tag)
                try:
                    self.validate(value)
                    return value
                except TagValidationError:
                    continue
        return None