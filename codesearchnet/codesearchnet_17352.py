def getaccesskey(self, window_name, object_name):
        """
        Get access key of given object

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: access key in string format on success, else LdtpExecutionError on failure.
        @rtype: string
        """
        # Used http://www.danrodney.com/mac/ as reference for
        # mapping keys with specific control
        # In Mac noticed (in accessibility inspector) only menu had access keys
        # so, get the menu_handle of given object and
        # return the access key
        menu_handle = self._get_menu_handle(window_name, object_name)
        key = menu_handle.AXMenuItemCmdChar
        modifiers = menu_handle.AXMenuItemCmdModifiers
        glpyh = menu_handle.AXMenuItemCmdGlyph
        virtual_key = menu_handle.AXMenuItemCmdVirtualKey
        modifiers_type = ""
        if modifiers == 0:
            modifiers_type = "<command>"
        elif modifiers == 1:
            modifiers_type = "<shift><command>"
        elif modifiers == 2:
            modifiers_type = "<option><command>"
        elif modifiers == 3:
            modifiers_type = "<option><shift><command>"
        elif modifiers == 4:
            modifiers_type = "<ctrl><command>"
        elif modifiers == 6:
            modifiers_type = "<ctrl><option><command>"
        # Scroll up
        if virtual_key == 115 and glpyh == 102:
            modifiers = "<option>"
            key = "<cursor_left>"
        # Scroll down
        elif virtual_key == 119 and glpyh == 105:
            modifiers = "<option>"
            key = "<right>"
        # Page up
        elif virtual_key == 116 and glpyh == 98:
            modifiers = "<option>"
            key = "<up>"
        # Page down
        elif virtual_key == 121 and glpyh == 107:
            modifiers = "<option>"
            key = "<down>"
        # Line up
        elif virtual_key == 126 and glpyh == 104:
            key = "<up>"
        # Line down
        elif virtual_key == 125 and glpyh == 106:
            key = "<down>"
        # Noticed in  Google Chrome navigating next tab
        elif virtual_key == 124 and glpyh == 101:
            key = "<right>"
        # Noticed in  Google Chrome navigating previous tab
        elif virtual_key == 123 and glpyh == 100:
            key = "<left>"
        # List application in a window to Force Quit
        elif virtual_key == 53 and glpyh == 27:
            key = "<escape>"
        # FIXME:
        # * Instruments Menu View->Run Browser
        # modifiers==12 virtual_key==48 glpyh==2
        # * Terminal Menu Edit->Start Dictation
        # fn fn - glpyh==148 modifiers==24
        # * Menu Chrome->Clear Browsing Data in Google Chrome
        # virtual_key==51 glpyh==23 [Delete Left (like Backspace on a PC)]
        if not key:
            raise LdtpServerException("No access key associated")
        return modifiers_type + key