def handle_stream_features(self, stream, features):
        """Process incoming <stream:features/> element.

        [initiating entity only]
        """
        element = features.find(MECHANISMS_TAG)
        self.peer_sasl_mechanisms = []
        if element is None:
            return None
        for sub in element:
            if sub.tag != MECHANISM_TAG:
                continue
            self.peer_sasl_mechanisms.append(sub.text)

        if stream.authenticated or not self.peer_sasl_mechanisms:
            return StreamFeatureNotHandled("SASL", mandatory = True)

        username = self.settings.get("username")
        if not username:
            # TODO: other rules for s2s
            if stream.me.local:
                username = stream.me.local
            else:
                username = None
        self._sasl_authenticate(stream, username, self.settings.get("authzid"))
        return StreamFeatureHandled("SASL", mandatory = True)