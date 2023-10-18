def getobjectinfo(self, window_name, object_name):
        """
        Get object properties.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: list of properties
        @rtype: list
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
        props = []
        if obj_info:
            for obj_prop in obj_info.keys():
                if not obj_info[obj_prop] or obj_prop == "obj":
                    # Don't add object handle to the list
                    continue
                props.append(obj_prop)
        return props