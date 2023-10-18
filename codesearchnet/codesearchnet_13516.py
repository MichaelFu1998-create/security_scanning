def make_stream_tls_features(self, stream, features):
        """Update the <features/> element with StartTLS feature.

        [receving entity only]

        :Parameters:
            - `features`: the <features/> element of the stream.
        :Types:
            - `features`: :etree:`ElementTree.Element`

        :returns: update <features/> element.
        :returntype: :etree:`ElementTree.Element`
        """
        if self.stream and stream is not self.stream:
            raise ValueError("Single StreamTLSHandler instance can handle"
                                                            " only one stream")
        self.stream = stream
        if self.settings["starttls"] and not stream.tls_established:
            tls = ElementTree.SubElement(features, STARTTLS_TAG)
            if self.settings["tls_require"]:
                ElementTree.SubElement(tls, REQUIRED_TAG)
        return features