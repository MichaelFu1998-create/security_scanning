def _load_client_secrets(self, filename):
        """Loads client secrets from the given filename."""
        client_type, client_info = clientsecrets.loadfile(filename)
        if client_type != clientsecrets.TYPE_WEB:
            raise ValueError(
                'The flow specified in {0} is not supported.'.format(
                    client_type))

        self.client_id = client_info['client_id']
        self.client_secret = client_info['client_secret']