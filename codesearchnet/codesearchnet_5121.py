def get_object(cls, api_token, action_id):
        """
            Class method that will return a Action object by ID.
        """
        action = cls(token=api_token, id=action_id)
        action.load_directly()
        return action