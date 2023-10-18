def cancel(self, campaign_id):
        """
        Cancel a Regular or Plain-Text Campaign after you send, before all of
        your recipients receive it. This feature is included with MailChimp
        Pro.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        """
        self.campaign_id = campaign_id
        return self._mc_client._post(url=self._build_path(campaign_id, 'actions/cancel-send'))