def submit_form(self, form_selector, input_dict):
        """Populate and submit a form on the current page.

        Raises GoogleAuthError if form can not be submitted.
        """
        logger.info(
            'Submitting form on page %r', self._page.url.split('?')[0]
        )
        logger.info(
            'Page contains forms: %s',
            [elem.get('id') for elem in self._page.soup.select('form')]
        )
        try:
            form = self._page.soup.select(form_selector)[0]
        except IndexError:
            raise GoogleAuthError(
                'Failed to find form {!r} in page'.format(form_selector)
            )
        logger.info(
            'Page contains inputs: %s',
            [elem.get('id') for elem in form.select('input')]
        )
        for selector, value in input_dict.items():
            try:
                form.select(selector)[0]['value'] = value
            except IndexError:
                raise GoogleAuthError(
                    'Failed to find input {!r} in form'.format(selector)
                )
        try:
            self._page = self._browser.submit(form, self._page.url)
            self._page.raise_for_status()
        except requests.RequestException as e:
            raise GoogleAuthError('Failed to submit form: {}'.format(e))