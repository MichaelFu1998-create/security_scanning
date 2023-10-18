def getapplist(self):
        """
        Get all accessibility application name that are currently running

        @return: list of appliction name of string type on success.
        @rtype: list
        """
        app_list = []
        # Update apps list, before parsing the list
        self._update_apps()
        for gui in self._running_apps:
            name = gui.localizedName()
            # default type was objc.pyobjc_unicode
            # convert to Unicode, else exception is thrown
            # TypeError: "cannot marshal <type 'objc.pyobjc_unicode'> objects"
            try:
                name = unicode(name)
            except NameError:
                name = str(name)
            except UnicodeEncodeError:
                pass
            app_list.append(name)
        # Return unique application list
        return list(set(app_list))