def selectitem(self, window_name, object_name, item_name):
        """
        Select combo box / layered pane item
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_name: Item name to select
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        self._grabfocus(object_handle.AXWindow)
        try:
            object_handle.Press()
        except AttributeError:
            # AXPress doesn't work with Instruments
            # So did the following work around
            x, y, width, height = self._getobjectsize(object_handle)
            # Mouse left click on the object
            # Note: x + width/2, y + height / 2 doesn't work
            self.generatemouseevent(x + 5, y + 5, "b1c")
            self.wait(5)
            handle = self._get_sub_menu_handle(object_handle, item_name)
            x, y, width, height = self._getobjectsize(handle)
            # on OSX 10.7 default "b1c" doesn't work
            # so using "b1d", verified with Fusion test, this works
            self.generatemouseevent(x + 5, y + 5, "b1d")
            return 1
        # Required for menuitem to appear in accessibility list
        self.wait(1)
        menu_list = re.split(";", item_name)
        try:
            menu_handle = self._internal_menu_handler(object_handle, menu_list,
                                                      True)
            # Required for menuitem to appear in accessibility list
            self.wait(1)
            if not menu_handle.AXEnabled:
                raise LdtpServerException(u"Object %s state disabled" % \
                                          menu_list[-1])
            menu_handle.Press()
        except LdtpServerException:
            object_handle.activate()
            object_handle.sendKey(AXKeyCodeConstants.ESCAPE)
            raise
        return 1