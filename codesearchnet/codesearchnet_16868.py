def update_template_version(
        self,
        name,
        subject,
        template_id,
        version_id,
        text='',
        html=None,
        timeout=None
    ):
        """ API call to update a template version """
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

        return self._api_request(
            self.TEMPLATES_VERSION_ENDPOINT % (template_id, version_id),
            self.HTTP_PUT,
            payload=payload,
            timeout=timeout
        )