def create_from_settings(settings):
        """ Create a connection with given settings.

        Args:
            settings (dict): A dictionary of settings

        Returns:
            :class:`Connection`. The connection
        """
        return Connection(
            settings["url"], 
            settings["base_url"],
            settings["user"],
            settings["password"],
            authorizations = settings["authorizations"],
            debug = settings["debug"]
        )