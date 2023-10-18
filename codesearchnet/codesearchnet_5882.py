def resume(self, campaign_id):
        """
        Resume an RSS-Driven campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        """
        self.campaign_id = campaign_id
        return self._mc_client._post(url=self._build_path(campaign_id, 'actions/resume'))