def authenticate(self):
        """
        Authenticate against the NuHeat API
        """
        if self._session_id:
            _LOGGER.debug("Using existing NuHeat session")
            return

        _LOGGER.debug("Creating NuHeat session")
        post_data = {
            "Email": self.username,
            "Password": self.password,
            "application": "0"
        }
        data = self.request(config.AUTH_URL, method="POST", data=post_data)
        session_id = data.get("SessionId")
        if not session_id:
            raise Exception("Authentication error")

        self._session_id = session_id