def set_all(self, model, **tags):
        """Validate and set all known tags on a port."""
        for name, tag in self.tags.items():
            if name in tags:
                value = tags.pop(name)
                if value:
                    try:
                        tag.set(model, value)
                    except TagValidationError as e:
                        raise n_exc.BadRequest(
                            resource="tags",
                            msg="%s" % (e.message))