def selectindex(self, window_name, object_name, item_index):
        """
        Select combo box item / layered pane based on index
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param item_index: Item index to select
        @type object_name: integer

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
        # Required for menuitem to appear in accessibility list
        self.wait(2)
        if not object_handle.AXChildren:
            raise LdtpServerException(u"Unable to find menu")
        # Get AXMenu
        children = object_handle.AXChildren[0]
        if not children:
            raise LdtpServerException(u"Unable to find menu")
        children = children.AXChildren
        tmp_children = []
        for child in children:
            role, label = self._ldtpize_accessible(child)
            # Don't add empty label
            # Menu separator have empty label's
            if label:
                tmp_children.append(child)
        children = tmp_children
        length = len(children)
        try:
            if item_index < 0 or item_index > length:
                raise LdtpServerException(u"Invalid item index %d" % item_index)
            menu_handle = children[item_index]
            if not menu_handle.AXEnabled:
                raise LdtpServerException(u"Object %s state disabled" % menu_list[-1])
            self._grabfocus(menu_handle)
            x, y, width, height = self._getobjectsize(menu_handle)
            # on OSX 10.7 default "b1c" doesn't work
            # so using "b1d", verified with Fusion test, this works
            window = object_handle.AXWindow
            # For some reason,
            # self.generatemouseevent(x + 5, y + 5, "b1d")
            # doesn't work with Fusion settings
            # Advanced window, so work around with this
            # ldtp.selectindex('*Advanced', 'Automatic', 1)
            """
            Traceback (most recent call last):
               File "build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/utils.py", line 178, in _dispatch
                  return getattr(self, method)(*args)
               File "build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/combo_box.py", line 146, in selectindex
                  self.generatemouseevent(x + 5, y + 5, "b1d")
               File "build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/mouse.py", line 97, in generatemouseevent
                  window=self._get_front_most_window()
               File "build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/utils.py", line 185, in _get_front_most_window
                  front_app=atomac.NativeUIElement.getFrontmostApp()
               File "build/bdist.macosx-10.8-intel/egg/atomac/AXClasses.py", line 114, in getFrontmostApp
                  raise ValueError('No GUI application found.')
            ValueError: No GUI application found.
            """
            window.doubleClickMouse((x + 5, y + 5))
            # If menuitem already pressed, set child to None
            # So, it doesn't click back in combobox in finally block
            child = None
        finally:
            if child:
                child.Cancel()
        return 1