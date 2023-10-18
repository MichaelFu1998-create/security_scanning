def create_new_locale(
        self,
        template_id,
        locale,
        version_name,
        subject,
        text='',
        html='',
        timeout=None
    ):
        """ API call to create a new locale and version of a template """
        payload = {
            'locale': locale,
            'name': version_name,
            'subject': subject
        }

        if html:
            payload['html'] = html
        if text:
            payload['text'] = text

        return self._api_request(
            self.TEMPLATES_LOCALES_ENDPOINT % template_id,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )