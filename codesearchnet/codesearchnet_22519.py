def handle_data(self, data):
        """
        Djeffify data between tags
        """
        if data.strip():
            data = djeffify_string(data)
        self.djhtml += data