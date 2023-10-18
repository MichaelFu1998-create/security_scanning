def make_stream_features(self, stream, features):
        """Add SASL features to the <features/> element of the stream.

        [receving entity only]

        :returns: update <features/> element."""
        mechs = self.settings['sasl_mechanisms']
        if mechs and not stream.authenticated:
            sub = ElementTree.SubElement(features, MECHANISMS_TAG)
            for mech in mechs:
                if mech in sasl.SERVER_MECHANISMS:
                    ElementTree.SubElement(sub, MECHANISM_TAG).text = mech
        return features