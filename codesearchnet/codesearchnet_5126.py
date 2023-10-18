def _perform_action(self, params, return_dict=True):
        """
            Perform a droplet action.

            Args:
                params (dict): parameters of the action

            Optional Args:
                return_dict (bool): Return a dict when True (default),
                    otherwise return an Action.

            Returns dict or Action
        """
        action = self.get_data(
            "droplets/%s/actions/" % self.id,
            type=POST,
            params=params
        )
        if return_dict:
            return action
        else:
            action = action[u'action']
            return_action = Action(token=self.token)
            # Loading attributes
            for attr in action.keys():
                setattr(return_action, attr, action[attr])
            return return_action