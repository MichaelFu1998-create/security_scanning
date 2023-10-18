def get_messages(self, params={}):
        """
        List messages

        http://dev.wheniwork.com/#listing-messages
        """
        param_list = [(k, params[k]) for k in sorted(params)]
        url = "/2/messages/?%s" % urlencode(param_list)

        data = self._get_resource(url)
        messages = []
        for entry in data["messages"]:
            messages.append(self.message_from_json(entry))

        return messages