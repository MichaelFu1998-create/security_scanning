def mouserightclick(self, window_name, object_name):
        """
        Mouse right click on an object.
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        self._grabfocus(object_handle)
        x, y, width, height = self._getobjectsize(object_handle)
        # Mouse right click on the object
        object_handle.clickMouseButtonRight((x + width / 2, y + height / 2))
        return 1