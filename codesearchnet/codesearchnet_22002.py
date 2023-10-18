def create_message(self, params={}):
        """
        Creates a message

        http://dev.wheniwork.com/#create/update-message
        """
        url = "/2/messages/"
        body = params

        data = self._post_resource(url, body)
        return self.message_from_json(data["message"])