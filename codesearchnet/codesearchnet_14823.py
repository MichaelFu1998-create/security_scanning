def pop(self, model):
        """Pop all matching tags off the port, return a valid one."""
        tags = self._pop(model)
        if tags:
            for tag in tags:
                value = self.deserialize(tag)
                try:
                    self.validate(value)
                    return value
                except TagValidationError:
                    continue