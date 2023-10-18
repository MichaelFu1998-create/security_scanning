def add_option(self, value, label):
        """Add an option for the field.

        :Parameters:
            - `value`: option values.
            - `label`: option label (human-readable description).
        :Types:
            - `value`: `list` of `unicode`
            - `label`: `unicode`
        """
        if type(value) is list:
            warnings.warn(".add_option() accepts single value now.", DeprecationWarning, stacklevel=1)
            value = value[0]
        if self.type not in ("list-multi", "list-single"):
            raise ValueError("Options are allowed only for list types.")
        option = Option(value, label)
        self.options.append(option)
        return option