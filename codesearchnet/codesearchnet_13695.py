def _make_stream_features(self):
        """Create the <features/> element for the stream.

        [receving entity only]

        :returns: new <features/> element
        :returntype: :etree:`ElementTree.Element`"""
        features = ElementTree.Element(FEATURES_TAG)
        for handler in self._stream_feature_handlers:
            handler.make_stream_features(self, features)
        return features