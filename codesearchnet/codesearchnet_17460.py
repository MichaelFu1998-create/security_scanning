def onedown(self, window_name, object_name, iterations):
        """
        Press scrollbar down with number of iterations

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string
        @param interations: iterations to perform on slider increase
        @type iterations: integer

        @return: 1 on success.
        @rtype: integer
        """
        if not self.verifyscrollbarvertical(window_name, object_name):
            raise LdtpServerException('Object not vertical scrollbar')
        object_handle = self._get_object_handle(window_name, object_name)
        i = 0
        maxValue = 1.0 / 8
        flag = False
        while i < iterations:
            if object_handle.AXValue >= 1:
                raise LdtpServerException('Maximum limit reached')
            object_handle.AXValue += maxValue
            time.sleep(1.0 / 100)
            flag = True
            i += 1
        if flag:
            return 1
        else:
            raise LdtpServerException('Unable to increase scrollbar')