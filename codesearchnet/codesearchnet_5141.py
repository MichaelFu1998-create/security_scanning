def get_object(cls, api_token):
        """
            Class method that will return an Account object.
        """
        acct = cls(token=api_token)
        acct.load()
        return acct