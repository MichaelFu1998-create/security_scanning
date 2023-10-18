def update(self, campaign_id, data):
        """
        Update some or all of the settings for a specific campaign.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "settings": object*
            {
                "subject_line": string*,
                "from_name": string*,
                "reply_to": string*
            },
        }
        """
        self.campaign_id = campaign_id
        if 'settings' not in data:
            raise KeyError('The campaign must have settings')
        if 'subject_line' not in data['settings']:
            raise KeyError('The campaign settings must have a subject_line')
        if 'from_name' not in data['settings']:
            raise KeyError('The campaign settings must have a from_name')
        if 'reply_to' not in data['settings']:
            raise KeyError('The campaign settings must have a reply_to')
        check_email(data['settings']['reply_to'])
        return self._mc_client._patch(url=self._build_path(campaign_id), data=data)