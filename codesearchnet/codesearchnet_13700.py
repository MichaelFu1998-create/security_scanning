def process_stream_error(self, error):
        """Process stream error element received.

        :Parameters:
            - `error`: error received

        :Types:
            - `error`: `StreamErrorElement`
        """
        # pylint: disable-msg=R0201
        logger.debug("Unhandled stream error: condition: {0} {1!r}"
                            .format(error.condition_name, error.serialize()))