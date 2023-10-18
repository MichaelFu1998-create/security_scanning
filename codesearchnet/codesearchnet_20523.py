def signed_session(self, session=None):
        """Create requests session with any required auth headers
        applied.

        :rtype: requests.Session.
        """

        if session:
            session = super(ClientCertAuthentication, self).signed_session(session)
        else:
            session = super(ClientCertAuthentication, self).signed_session()

        if self.cert is not None:
            session.cert = self.cert
        if self.ca_cert is not None:
            session.verify = self.ca_cert
        if self.no_verify:
            session.verify = False

        return session