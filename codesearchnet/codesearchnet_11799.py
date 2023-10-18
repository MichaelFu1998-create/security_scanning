def all_other_enabled_satchels(self):
        """
        Returns a dictionary of satchels used in the current configuration, excluding ourselves.
        """
        return dict(
            (name, satchel)
            for name, satchel in self.all_satchels.items()
            if name != self.name.upper() and name.lower() in map(str.lower, self.genv.services)
        )