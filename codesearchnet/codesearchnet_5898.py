def create(self, data):
        """
        Add a new store to your MailChimp account.

        Error checking on the currency code verifies that it is in the correct
        three-letter, all-caps format as specified by ISO 4217 but does not
        check that it is a valid code as the list of valid codes changes over
        time.

        :param data: The request body parameters
        :type data: :py:class:`dict`
        data = {
            "id": string*,
            "list_id": string*,
            "name": string*,
            "currency_code": string*
        }
        """
        if 'id' not in data:
            raise KeyError('The store must have an id')
        if 'list_id' not in data:
            raise KeyError('The store must have a list_id')
        if 'name' not in data:
            raise KeyError('The store must have a name')
        if 'currency_code' not in data:
            raise KeyError('The store must have a currency_code')
        if not re.match(r"^[A-Z]{3}$", data['currency_code']):
            raise ValueError('The currency_code must be a valid 3-letter ISO 4217 currency code')
        response = self._mc_client._post(url=self._build_path(), data=data)
        if response is not None:
            self.store_id = response['id']
        else:
            self.store_id = None
        return response