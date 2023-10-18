def enterstring(self, window_name, object_name='', data=''):
        """
        Type string sequence.
        
        @param window_name: Window name to focus on, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to focus on, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param data: data to type.
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        if not object_name and not data:
            return self.generatekeyevent(window_name)
        else:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                raise LdtpServerException(u"Object %s state disabled" % object_name)
            self._grabfocus(object_handle)
            object_handle.sendKeys(data)
            return 1