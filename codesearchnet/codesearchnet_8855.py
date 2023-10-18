def lrs(self):
        """
        LRS client instance to be used for sending statements.
        """
        return RemoteLRS(
            version=self.lrs_configuration.version,
            endpoint=self.lrs_configuration.endpoint,
            auth=self.lrs_configuration.authorization_header,
        )