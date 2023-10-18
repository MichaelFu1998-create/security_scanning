def create_template(
        self,
        name,
        subject,
        html,
        text='',
        timeout=None
    ):
        """ API call to create a template """
        payload = {
            'name': name,
            'subject': subject,
            'html': html,
            'text': text
        }

        return self._api_request(
            self.TEMPLATES_ENDPOINT,
            self.HTTP_POST,
            payload=payload,
            timeout=timeout
        )