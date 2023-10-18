def all(self, campaign_id, get_all=False, **queryparams):
        """
        Get information about members who have unsubscribed from a specific
        campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param get_all: Should the query get all results
        :type get_all: :py:class:`bool`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        queryparams['count'] = integer
        queryparams['offset'] = integer
        """
        self.campaign_id = campaign_id
        self.subscriber_hash = None
        if get_all:
            return self._iterate(url=self._build_path(campaign_id, 'unsubscribed'), **queryparams)
        else:
            return self._mc_client._get(url=self._build_path(campaign_id, 'unsubscribed'), **queryparams)