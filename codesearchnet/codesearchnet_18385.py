def _add_option(self, option):
        """Add an Option object to the user interface."""
        if option.name in self.options:
            raise ValueError('name already in use')
        if option.abbreviation in self.abbreviations:
            raise ValueError('abbreviation already in use')
        if option.name in [arg.name for arg in self.positional_args]:
            raise ValueError('name already in use by a positional argument')
        self.options[option.name] = option
        if option.abbreviation:
            self.abbreviations[option.abbreviation] = option
        self.option_order.append(option.name)