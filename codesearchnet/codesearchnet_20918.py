def _get_password_url(self):
        """ Get URL used for authentication

        Returns:
            string: URL
        """
        password_url = None
        if self._settings["user"] or self._settings["authorization"]:
            if self._settings["url"]:
                password_url = self._settings["url"]
            elif self._settings["base_url"]:
                password_url = self._settings["base_url"]
        return password_url