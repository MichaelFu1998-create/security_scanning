def get_stream(self, error_callback=None, live=True):
        """ Get room stream to listen for messages.

        Kwargs:
            error_callback (func): Callback to call when an error occurred (parameters: exception)
            live (bool): If True, issue a live stream, otherwise an offline stream

        Returns:
            :class:`Stream`. Stream
        """
        self.join()
        return Stream(self, error_callback=error_callback, live=live)