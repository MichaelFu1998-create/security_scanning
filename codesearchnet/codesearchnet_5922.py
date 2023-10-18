def create(self, data):
        """
        Create a new MailChimp campaign.

        The ValueError raised by an invalid type in data does not mention
        'absplit' as a potential value because the documentation indicates
        that the absplit type has been deprecated.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "recipients": object*
            {
                "list_id": string*
            },
            "settings": object*
            {
                "subject_line": string*,
                "from_name": string*,
                "reply_to": string*
            },
            "variate_settings": object* (Required if type is "variate")
            {
                "winner_criteria": string* (Must be one of "opens", "clicks", "total_revenue", or "manual")
            },
            "rss_opts": object* (Required if type is "rss")
            {
                "feed_url": string*,
                "frequency": string* (Must be one of "daily", "weekly", or "monthly")
            },
            "type": string* (Must be one of "regular", "plaintext", "rss", "variate", or "absplit")
        }
        """
        if 'recipients' not in data:
            raise KeyError('The campaign must have recipients')
        if 'list_id' not in data['recipients']:
            raise KeyError('The campaign recipients must have a list_id')
        if 'settings' not in data:
            raise KeyError('The campaign must have settings')
        if 'subject_line' not in data['settings']:
            raise KeyError('The campaign settings must have a subject_line')
        if 'from_name' not in data['settings']:
            raise KeyError('The campaign settings must have a from_name')
        if 'reply_to' not in data['settings']:
            raise KeyError('The campaign settings must have a reply_to')
        check_email(data['settings']['reply_to'])
        if 'type' not in data:
            raise KeyError('The campaign must have a type')
        if not data['type'] in ['regular', 'plaintext', 'rss', 'variate', 'abspilt']:
            raise ValueError('The campaign type must be one of "regular", "plaintext", "rss", or "variate"')
        if data['type'] == 'variate':
            if 'variate_settings' not in data:
                raise KeyError('The variate campaign must have variate_settings')
            if 'winner_criteria' not in data['variate_settings']:
                raise KeyError('The campaign variate_settings must have a winner_criteria')
            if data['variate_settings']['winner_criteria'] not in ['opens', 'clicks', 'total_revenue', 'manual']:
                raise ValueError('The campaign variate_settings '
                                 'winner_criteria must be one of "opens", "clicks", "total_revenue", or "manual"')
        if data['type'] == 'rss':
            if 'rss_opts' not in data:
                raise KeyError('The rss campaign must have rss_opts')
            if 'feed_url' not in data['rss_opts']:
                raise KeyError('The campaign rss_opts must have a feed_url')
            if not data['rss_opts']['frequency'] in ['daily', 'weekly', 'monthly']:
                raise ValueError('The rss_opts frequency must be one of "daily", "weekly", or "monthly"')
        response = self._mc_client._post(url=self._build_path(), data=data)
        if response is not None:
            self.campaign_id = response['id']
        else:
            self.campaign_id = None
        return response