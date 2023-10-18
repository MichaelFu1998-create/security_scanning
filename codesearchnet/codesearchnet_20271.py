def send(self, send_email=True):
        """Marks the invoice as sent in Holvi

        If send_email is False then the invoice is *not* automatically emailed to the recipient
        and your must take care of sending the invoice yourself.
        """
        url = str(self.api.base_url + '{code}/status/').format(code=self.code)  # six.u messes this up
        payload = {
            'mark_as_sent': True,
            'send_email': send_email,
        }
        stat = self.api.connection.make_put(url, payload)