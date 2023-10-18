def get_users(self, params={}):
        """
        Returns a list of users.

        http://dev.wheniwork.com/#listing-users
        """
        param_list = [(k, params[k]) for k in sorted(params)]
        url = "/2/users/?%s" % urlencode(param_list)

        data = self._get_resource(url)
        users = []
        for entry in data["users"]:
            users.append(self.user_from_json(entry))

        return users