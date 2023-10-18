def update(self, list_id, data):
        """
        Update the settings for a specific list.

        :param list_id: The unique id for the list.
        :type list_id: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "name": string*,
            "contact": object*
            {
                "company": string*,
                "address1": string*,
                "city": string*,
                "state": string*,
                "zip": string*,
                "country": string*
            },
            "permission_reminder": string*,
            "campaign_defaults": object*
            {
                "from_name": string*,
                "from_email": string*,
                "subject": string*,
                "language": string*
            },
            "email_type_option": boolean
        }
        """
        self.list_id = list_id
        if 'name' not in data:
            raise KeyError('The list must have a name')
        if 'contact' not in data:
            raise KeyError('The list must have a contact')
        if 'company' not in data['contact']:
            raise KeyError('The list contact must have a company')
        if 'address1' not in data['contact']:
            raise KeyError('The list contact must have a address1')
        if 'city' not in data['contact']:
            raise KeyError('The list contact must have a city')
        if 'state' not in data['contact']:
            raise KeyError('The list contact must have a state')
        if 'zip' not in data['contact']:
            raise KeyError('The list contact must have a zip')
        if 'country' not in data['contact']:
            raise KeyError('The list contact must have a country')
        if 'permission_reminder' not in data:
            raise KeyError('The list must have a permission_reminder')
        if 'campaign_defaults' not in data:
            raise KeyError('The list must have a campaign_defaults')
        if 'from_name' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a from_name')
        if 'from_email' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a from_email')
        check_email(data['campaign_defaults']['from_email'])
        if 'subject' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a subject')
        if 'language' not in data['campaign_defaults']:
            raise KeyError('The list campaign_defaults must have a language')
        if 'email_type_option' not in data:
            raise KeyError('The list must have an email_type_option')
        if data['email_type_option'] not in [True, False]:
            raise TypeError('The list email_type_option must be True or False')
        return self._mc_client._patch(url=self._build_path(list_id), data=data)