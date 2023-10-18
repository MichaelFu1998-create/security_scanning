def configure(self, url=None, token=None, test=False):
        """
        Configure the api to use given url and token or to get them from the
        Config.
        """

        if url is None:
            url = Config.get_value("url")
        if token is None:
            token = Config.get_value("token")

        self.server_url = url
        self.auth_header = {"Authorization": "Basic {0}".format(token)}
        self.configured = True

        if test:
            self.test_connection()

        Config.set("url", url)
        Config.set("token", token)