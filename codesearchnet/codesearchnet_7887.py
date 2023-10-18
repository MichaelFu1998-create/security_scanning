def error(self, error_name, error_message, endpoint=None, msg_id=None,
              quiet=False):
        """Send an error to the user, using the custom or default
        ErrorHandler configured on the [TODO: Revise this] Socket/Handler
        object.

        :param error_name: is a simple string, for easy association on
                           the client side

        :param error_message: is a human readable message, the user
                              will eventually see

        :param endpoint: set this if you have a message specific to an
                         end point

        :param msg_id: set this if your error is relative to a
                       specific message

        :param quiet: way to make the error handler quiet. Specific to
                      the handler.  The default handler will only log,
                      with quiet.
        """
        handler = self.error_handler
        return handler(
            self, error_name, error_message, endpoint, msg_id, quiet)