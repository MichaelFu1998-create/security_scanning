def update_message(self, message):
        """
        Modify an existing message.

        http://dev.wheniwork.com/#create/update-message
        """
        url = "/2/messages/%s" % message.message_id

        data = self._put_resource(url, message.json_data())
        return self.message_from_json(data)