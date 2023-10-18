def listsubmenus(self, window_name, object_name):
        """
        List children of menu item
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: menu item in list on success.
        @rtype: list
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        role, label = self._ldtpize_accessible(menu_handle)
        menu_clicked = False
        try:
            if not menu_handle.AXChildren:
                menu_clicked = True
                try:
                    menu_handle.Press()
                    self.wait(1)
                except atomac._a11y.ErrorCannotComplete:
                    pass
                if not menu_handle.AXChildren:
                    raise LdtpServerException(u"Unable to find children under menu %s" % \
                                              label)
            children = menu_handle.AXChildren[0]
            sub_menus = []
            for current_menu in children.AXChildren:
                role, label = self._ldtpize_accessible(current_menu)
                if not label:
                    # All splitters have empty label
                    continue
                sub_menus.append(u"%s%s" % (role, label))
        finally:
            if menu_clicked:
                menu_handle.Cancel()
        return sub_menus