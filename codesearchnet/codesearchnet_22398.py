def load_values(self):
        """
        Go through the env var map, transferring the values to this object
        as attributes.

        :raises: RuntimeError if a required env var isn't defined.
        """

        for config_name, evar in self.evar_defs.items():
            if evar.is_required and evar.name not in os.environ:
                raise RuntimeError((
                    "Missing required environment variable: {evar_name}\n"
                    "{help_txt}"
                ).format(evar_name=evar.name, help_txt=evar.help_txt))
            # Env var is present. Transfer its value over.
            if evar.name in os.environ:
                self[config_name] = os.environ.get(evar.name)
            else:
                self[config_name] = evar.default_val
            # Perform any validations or transformations.
            for filter in evar.filters:
                current_val = self.get(config_name)
                new_val = filter(current_val, evar)
                self[config_name] = new_val
        # This is the top-level filter that is often useful for checking
        # the values of related env vars (instead of individual validation).
        self._filter_all()