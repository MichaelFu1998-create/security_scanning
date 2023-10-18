def create(self, campaign_id, data, **queryparams):
        """
        Add feedback on a specific campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "message": string*
        }
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        """
        self.campaign_id = campaign_id
        if 'message' not in data:
            raise KeyError('The campaign feedback must have a message')
        response = self._mc_client._post(url=self._build_path(campaign_id, 'feedback'), data=data, **queryparams)
        if response is not None:
            self.feedback_id = response['feedback_id']
        else:
            self.feedback_id = None
        return response