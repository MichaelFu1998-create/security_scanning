def update(self, campaign_id, data):
        """
        Set the content for a campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        """
        self.campaign_id = campaign_id
        return self._mc_client._put(url=self._build_path(campaign_id, 'content'), data=data)