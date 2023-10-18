def handle_stream_features(self, stream, features):
        """Process incoming StartTLS related element of <stream:features/>.

        [initiating entity only]

        """
        if self.stream and stream is not self.stream:
            raise ValueError("Single StreamTLSHandler instance can handle"
                                                            " only one stream")
        self.stream = stream
        logger.debug(" tls: handling features")
        element = features.find(STARTTLS_TAG)
        if element is None:
            logger.debug(" tls: no starttls feature found")
            if self.settings["tls_require"]:
                raise TLSNegotiationFailed("StartTLS required,"
                                                " but not supported by peer")
            return None
        if len(features) == 1:
            required = True
        else:
            required = element.find(REQUIRED_TAG) is not None
        if stream.tls_established:
            logger.warning("StartTLS offerred when already established")
            return StreamFeatureNotHandled("StartTLS", mandatory = required)

        if self.settings["starttls"]:
            logger.debug("StartTLS negotiated")
            self._request_tls()
            return StreamFeatureHandled("StartTLS", mandatory = required)
        else:
            logger.debug(" tls: not enabled")
            return StreamFeatureNotHandled("StartTLS", mandatory = required)