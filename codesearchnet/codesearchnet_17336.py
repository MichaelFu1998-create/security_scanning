def getobjectproperty(self, window_name, object_name, prop):
        """
        Get object property value.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string
        @param prop: property name.
        @type prop: string

        @return: property
        @rtype: string
        """
        try:
            obj_info = self._get_object_map(window_name, object_name,
                                            wait_for_object=False)
        except atomac._a11y.ErrorInvalidUIElement:
            # During the test, when the window closed and reopened
            # ErrorInvalidUIElement exception will be thrown
            self._windows = {}
            # Call the method again, after updating apps
            obj_info = self._get_object_map(window_name, object_name,
                                            wait_for_object=False)
        if obj_info and prop != "obj" and prop in obj_info:
            if prop == "class":
                # ldtp_class_type are compatible with Linux and Windows class name
                # If defined class name exist return that,
                # else return as it is
                return ldtp_class_type.get(obj_info[prop], obj_info[prop])
            else:
                return obj_info[prop]
        raise LdtpServerException('Unknown property "%s" in %s' % \
                                  (prop, object_name))