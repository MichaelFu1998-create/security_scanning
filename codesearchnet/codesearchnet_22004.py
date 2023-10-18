def delete_messages(self, messages):
        """
        Delete existing messages.

        http://dev.wheniwork.com/#delete-existing-message
        """
        url = "/2/messages/?%s" % urlencode([('ids', ",".join(messages))])

        data = self._delete_resource(url)
        return data