def scrolldown(self, window_name, object_name):
        """
        Scroll down

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        if not self.verifyscrollbarvertical(window_name, object_name):
            raise LdtpServerException('Object not vertical scrollbar')
        return self.setmax(window_name, object_name)