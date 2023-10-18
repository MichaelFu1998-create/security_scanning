def get_by_username(self, username):
        """Retrieve user by username"""
        res = filter(lambda x: x.username == username, self.users.values())
        if len(res) > 0:
            return res[0]
        return None