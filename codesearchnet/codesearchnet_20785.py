def add_ctl_field(self, name, value):
        """
        Add new control field `value` with under `name` into control field
        dictionary :attr:`controlfields`.
        """
        if len(name) != 3:
            raise ValueError("name parameter have to be exactly 3 chars long!")

        self.controlfields[name] = value