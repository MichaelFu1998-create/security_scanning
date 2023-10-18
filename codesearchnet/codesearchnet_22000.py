def get_message(self, message_id):
        """
        Get Existing Message

        http://dev.wheniwork.com/#get-existing-message
        """
        url = "/2/messages/%s" % message_id

        return self.message_from_json(self._get_resource(url)["message"])