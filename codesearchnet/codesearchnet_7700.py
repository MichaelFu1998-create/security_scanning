def login(self):
        """
        Login to the router.

        Will be called automatically by other actions.
        """
        if not self.force_login_v2:
            v1_result = self.login_v1()
            if v1_result:
                return v1_result

        return self.login_v2()