def get_user(self, user_id):
        """
        Returns user profile data.

        http://dev.wheniwork.com/#get-existing-user
        """
        url = "/2/users/%s" % user_id

        return self.user_from_json(self._get_resource(url)["user"])