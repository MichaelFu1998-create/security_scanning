def make_stream_features(self, stream, features):
        """Add resource binding feature to the <features/> element of the
        stream.

        [receving entity only]

        :returns: update <features/> element.
        """
        self.stream = stream
        if stream.peer_authenticated and not stream.peer.resource:
            ElementTree.SubElement(features, FEATURE_BIND)