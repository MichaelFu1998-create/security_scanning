def check(self):
        """
        Run inadyn from the commandline to test the configuration.

        To be run like:

            fab role inadyn.check

        """
        self._validate_settings()
        r = self.local_renderer
        r.env.alias = r.env.aliases[0]
        r.sudo(r.env.check_command_template)