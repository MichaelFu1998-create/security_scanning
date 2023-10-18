def getallstates(self, window_name, object_name):
        """
        Get all states of given object

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: list of string on success.
        @rtype: list
        """
        object_handle = self._get_object_handle(window_name, object_name)
        _obj_states = []
        if object_handle.AXEnabled:
            _obj_states.append("enabled")
        if object_handle.AXFocused:
            _obj_states.append("focused")
        else:
            try:
                if object_handle.AXFocused:
                    _obj_states.append("focusable")
            except:
                pass
        if re.match("AXCheckBox", object_handle.AXRole, re.M | re.U | re.L) or \
                re.match("AXRadioButton", object_handle.AXRole,
                         re.M | re.U | re.L):
            if object_handle.AXValue:
                _obj_states.append("checked")
        return _obj_states