def create_new_version(
        self,
        name,
        subject,
        text='',
        template_id=None,
        html=None,
        locale=None,
        timeout=None
    ):
        """ API call to create a new version of a template """
        if(html):
            payload = {
                'name': name,
                'subject': subject,
                'html': html,
                'text': text
            }
        else:
            payload = {
                'name': name,
                'subject': subject,
                'text': text
            }

        if locale:
            url = self.TEMPLATES_SPECIFIC_LOCALE_VERSIONS_ENDPOINT % (
                template_id,
                locale
            )
        else:
            url = self.TEMPLATES_NEW_VERSION_ENDPOINT % template_id

        return self._api_request(
            url,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )