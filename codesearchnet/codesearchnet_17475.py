def getallitem(self, window_name, object_name):
        """
        Get all combo box item

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: list of string on success.
        @rtype: list
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        object_handle.Press()
        # Required for menuitem to appear in accessibility list
        self.wait(1)
        child = None
        try:
            if not object_handle.AXChildren:
                raise LdtpServerException(u"Unable to find menu")
            # Get AXMenu
            children = object_handle.AXChildren[0]
            if not children:
                raise LdtpServerException(u"Unable to find menu")
            children = children.AXChildren
            items = []
            for child in children:
                label = self._get_title(child)
                # Don't add empty label
                # Menu separator have empty label's
                if label:
                    items.append(label)
        finally:
            if child:
                # Set it back, by clicking combo box
                child.Cancel()
        return items