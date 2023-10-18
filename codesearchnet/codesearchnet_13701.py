def _got_features(self, features):
        """Process incoming <stream:features/> element.

        [initiating entity only]

        The received features node is available in `features`."""
        self.features = features
        logger.debug("got features, passing to event handlers...")
        handled = self.event(GotFeaturesEvent(self.features))
        logger.debug("  handled: {0}".format(handled))
        if not handled:
            mandatory_handled = []
            mandatory_not_handled = []
            logger.debug("  passing to stream features handlers: {0}"
                                    .format(self._stream_feature_handlers))
            for handler in self._stream_feature_handlers:
                ret = handler.handle_stream_features(self, self.features)
                if ret is None:
                    continue
                elif isinstance(ret, StreamFeatureHandled):
                    if ret.mandatory:
                        mandatory_handled.append(unicode(ret))
                        break
                    break
                elif isinstance(ret, StreamFeatureNotHandled):
                    if ret.mandatory:
                        mandatory_not_handled.append(unicode(ret))
                        break
                else:
                    raise ValueError("Wrong value returned from a stream"
                            " feature handler: {0!r}".format(ret))
            if mandatory_not_handled and not mandatory_handled:
                self.send_stream_error("unsupported-feature")
                raise FatalStreamError(
                        u"Unsupported mandatory-to-implement features: "
                                        + u" ".join(mandatory_not_handled))