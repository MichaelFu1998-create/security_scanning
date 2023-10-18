def delete(self, campaign_id):
        """
        Remove a campaign from your MailChimp account.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        """
        self.campaign_id = campaign_id
        return self._mc_client._delete(url=self._build_path(campaign_id))