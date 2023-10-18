def get_action(self, action_id):
        """Returns a specific Action by its ID.

        Args:
            action_id (int): id of action
        """
        return Action.get_object(
            api_token=self.token,
            action_id=action_id
        )