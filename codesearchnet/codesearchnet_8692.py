def get_actor(self, username, email):
        """
        Get actor for the statement.
        """
        return Agent(
            name=username,
            mbox='mailto:{email}'.format(email=email),
        )