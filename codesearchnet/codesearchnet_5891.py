def update(self, campaign_id, feedback_id, data):
        """
        Update a specific feedback message for a campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param feedback_id: The unique id for the feedback message.
        :type feedback_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "message": string*
        }
        """
        self.campaign_id = campaign_id
        self.feedback_id = feedback_id
        if 'message' not in data:
            raise KeyError('The campaign feedback must have a message')
        return self._mc_client._patch(url=self._build_path(campaign_id, 'feedback', feedback_id), data=data)