def send(self, campaign_id):
        """
        Send a MailChimp campaign. For RSS Campaigns, the campaign will send
        according to its schedule. All other campaigns will send immediately.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        """
        self.campaign_id = campaign_id
        return self._mc_client._post(url=self._build_path(campaign_id, 'actions/send'))