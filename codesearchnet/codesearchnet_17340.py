def click(self, window_name, object_name):
        """
        Click item.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        size = self._getobjectsize(object_handle)
        self._grabfocus(object_handle)
        self.wait(0.5)

        # If object doesn't support Press, trying clicking with the object
        # coordinates, where size=(x, y, width, height)
        # click on center of the widget
        # Noticed this issue on clicking AXImage
        # click('Instruments*', 'Automation')
        self.generatemouseevent(size[0] + size[2] / 2, size[1] + size[3] / 2, "b1c")
        return 1