def get_requests(self, params={}):
        """
        List requests

        http://dev.wheniwork.com/#listing-requests
        """
        if "status" in params:
            params['status'] = ','.join(map(str, params['status']))

        requests = []
        users = {}
        messages = {}
        params['page'] = 0
        while True:
            param_list = [(k, params[k]) for k in sorted(params)]
            url = "/2/requests/?%s" % urlencode(param_list)

            data = self._get_resource(url)
            for entry in data["users"]:
                user = Users.user_from_json(entry)
                users[user.user_id] = user
            for entry in data["requests"]:
                request = self.request_from_json(entry)
                requests.append(request)
            for entry in data["messages"]:
                message = Messages.message_from_json(entry)
                if message.request_id not in messages:
                    messages[message.request_id] = []
                messages[message.request_id].append(message)

            if not data['more']:
                break

            params['page'] += 1

        for request in requests:
            request.user = users.get(request.user_id, None)
            request.messages = messages.get(request.request_id, [])

        return requests