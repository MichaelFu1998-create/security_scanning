def handle_date_mismatch(self, req):
        """
        Handle a request whose date doesn't match the signing key scope date.

        This AWS4Auth class implementation regenerates the signing key. See
        StrictAWS4Auth class if you would prefer an exception to be raised.

        req -- a requests prepared request object

        """
        req_datetime = self.get_request_date(req)
        new_key_date = req_datetime.strftime('%Y%m%d')
        self.regenerate_signing_key(date=new_key_date)