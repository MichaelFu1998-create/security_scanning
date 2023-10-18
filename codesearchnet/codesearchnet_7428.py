def update_items(self, payload):
        """
        Update existing items
        Accepts one argument, a list of dicts containing Item data
        """
        to_send = [self.check_items([p])[0] for p in payload]
        headers = {}
        headers.update(self.default_headers())
        # the API only accepts 50 items at a time, so we have to split
        # anything longer
        for chunk in chunks(to_send, 50):
            req = requests.post(
                url=self.endpoint
                + "/{t}/{u}/items/".format(t=self.library_type, u=self.library_id),
                headers=headers,
                data=json.dumps(chunk),
            )
            self.request = req
            try:
                req.raise_for_status()
            except requests.exceptions.HTTPError:
                error_handler(req)
            return True