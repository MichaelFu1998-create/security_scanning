def is_public(self):
        """Return True iff this method should be considered public."""
        # Check if we are a setter/deleter method, and mark as private if so.
        for decorator in self.decorators:
            # Given 'foo', match 'foo.bar' but not 'foobar' or 'sfoo'
            if re.compile(r"^{}\.".format(self.name)).match(decorator.name):
                return False
        name_is_public = (
            not self.name.startswith("_")
            or self.name in VARIADIC_MAGIC_METHODS
            or self.is_magic
        )
        return self.parent.is_public and name_is_public