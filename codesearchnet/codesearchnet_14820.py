def set(self, model, value):
        """Set tag on model object."""
        self.validate(value)
        self._pop(model)
        value = self.serialize(value)
        model.tags.append(value)