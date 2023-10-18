def get_headers(self):
        """ Get headers.

        Returns:
            tuple: Headers
        """
        headers = {
            "User-Agent": "kFlame 1.0"
        }

        password_url = self._get_password_url()
        if password_url and password_url in self._settings["authorizations"]:
            headers["Authorization"] = self._settings["authorizations"][password_url]

        return headers