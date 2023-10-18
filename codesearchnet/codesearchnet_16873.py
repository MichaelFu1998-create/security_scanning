def send(
        self,
        email_id,
        recipient,
        email_data=None,
        sender=None,
        cc=None,
        bcc=None,
        tags=[],
        headers={},
        esp_account=None,
        locale=None,
        email_version_name=None,
        inline=None,
        files=[],
        timeout=None
    ):
        """ API call to send an email """
        if not email_data:
            email_data = {}

        # for backwards compatibility, will be removed
        if isinstance(recipient, string_types):
            warnings.warn(
                "Passing email directly for recipient is deprecated",
                DeprecationWarning)
            recipient = {'address': recipient}

        payload = {
            'email_id': email_id,
            'recipient': recipient,
            'email_data': email_data
        }

        if sender:
            payload['sender'] = sender
        if cc:
            if not type(cc) == list:
                logger.error(
                    'kwarg cc must be type(list), got %s' % type(cc))
            payload['cc'] = cc
        if bcc:
            if not type(bcc) == list:
                logger.error(
                    'kwarg bcc must be type(list), got %s' % type(bcc))
            payload['bcc'] = bcc

        if tags:
            if not type(tags) == list:
                logger.error(
                    'kwarg tags must be type(list), got %s' % (type(tags)))
            payload['tags'] = tags

        if headers:
            if not type(headers) == dict:
                logger.error(
                    'kwarg headers must be type(dict), got %s' % (
                        type(headers)
                    )
                )
            payload['headers'] = headers

        if esp_account:
            if not isinstance(esp_account, string_types):
                logger.error(
                    'kwarg esp_account must be a string, got %s' % (
                        type(esp_account)
                    )
                )
            payload['esp_account'] = esp_account

        if locale:
            if not isinstance(locale, string_types):
                logger.error(
                    'kwarg locale must be a string, got %s' % (type(locale))
                )
            payload['locale'] = locale

        if email_version_name:
            if not isinstance(email_version_name, string_types):
                logger.error(
                    'kwarg email_version_name must be a string, got %s' % (
                        type(email_version_name)))
            payload['version_name'] = email_version_name

        if inline:
            payload['inline'] = self._make_file_dict(inline)

        if files:
            payload['files'] = [self._make_file_dict(f) for f in files]

        return self._api_request(
            self.SEND_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )