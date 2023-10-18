def verifyselect(self, window_name, object_name, item_name):
        """
        Verify the item selected in combo box
        
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
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                return 0
            role, label = self._ldtpize_accessible(object_handle)
            title = self._get_title(object_handle)
            if re.match(item_name, title, re.M | re.U | re.L) or \
                    re.match(item_name, label, re.M | re.U | re.L) or \
                    re.match(item_name, u"%u%u" % (role, label),
                             re.M | re.U | re.L):
                return 1
        except LdtpServerException:
            pass
        return 0