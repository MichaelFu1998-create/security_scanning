def error(self, error_name, error_message, msg_id=None, quiet=False):
        """Use this to use the configured ``error_handler`` yield an
        error message to your application.

        :param error_name: is a short string, to associate messages to recovery
                           methods
        :param error_message: is some human-readable text, describing the error
        :param msg_id: is used to associate with a request
        :param quiet: specific to error_handlers. The default doesn't send a
                      message to the user, but shows a debug message on the
                      developer console.
        """
        self.socket.error(error_name, error_message, endpoint=self.ns_name,
                          msg_id=msg_id, quiet=quiet)