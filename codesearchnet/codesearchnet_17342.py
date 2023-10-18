def hasstate(self, window_name, object_name, state, guiTimeOut=0):
        """
        has state

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string
        @type window_name: string
        @param state: State of the current object.
        @type object_name: string
        @param guiTimeOut: Wait timeout in seconds
        @type guiTimeOut: integer

        @return: 1 on success.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if state == "enabled":
                return int(object_handle.AXEnabled)
            elif state == "focused":
                return int(object_handle.AXFocused)
            elif state == "focusable":
                return int(object_handle.AXFocused)
            elif state == "checked":
                if re.match("AXCheckBox", object_handle.AXRole,
                            re.M | re.U | re.L) or \
                        re.match("AXRadioButton", object_handle.AXRole,
                                 re.M | re.U | re.L):
                    if object_handle.AXValue:
                        return 1
        except:
            pass
        return 0