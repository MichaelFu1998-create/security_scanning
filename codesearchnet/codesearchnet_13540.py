def handle_stream_features(self, stream, features):
        """Process incoming <stream:features/> element.

        [initiating entity only]

        The received features element is available in `features`.
        """
        logger.debug(u"Handling stream features: {0}".format(
                                        element_to_unicode(features)))
        element = features.find(FEATURE_BIND)
        if element is None:
            logger.debug("No <bind/> in features")
            return None
        resource = stream.settings["resource"]
        self.bind(stream, resource)
        return StreamFeatureHandled("Resource binding", mandatory = True)