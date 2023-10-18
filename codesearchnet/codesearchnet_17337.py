def getchild(self, window_name, child_name='', role='', parent=''):
        """
        Gets the list of object available in the window, which matches
        component name or role name or both.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param child_name: Child name to search for.
        @type child_name: string
        @param role: role name to search for, or an empty string for wildcard.
        @type role: string
        @param parent: parent name to search for, or an empty string for wildcard.
        @type role: string
        @return: list of matched children names
        @rtype: list
        """
        matches = []
        if role:
            role = re.sub(' ', '_', role)
        self._windows = {}
        if parent and (child_name or role):
            _window_handle, _window_name = \
                self._get_window_handle(window_name)[0:2]
            if not _window_handle:
                raise LdtpServerException('Unable to find window "%s"' % \
                                          window_name)
            appmap = self._get_appmap(_window_handle, _window_name)
            obj = self._get_object_map(window_name, parent)

            def _get_all_children_under_obj(obj, child_list):
                if role and obj['class'] == role:
                    child_list.append(obj['label'])
                elif child_name and self._match_name_to_appmap(child_name, obj):
                    child_list.append(obj['label'])
                if obj:
                    children = obj['children']
                if not children:
                    return child_list
                for child in children.split():
                    return _get_all_children_under_obj( \
                        appmap[child],
                        child_list)

            matches = _get_all_children_under_obj(obj, [])
            if not matches:
                if child_name:
                    _name = 'name "%s" ' % child_name
                if role:
                    _role = 'role "%s" ' % role
                if parent:
                    _parent = 'parent "%s"' % parent
                exception = 'Could not find a child %s%s%s' % (_name, _role, _parent)
                raise LdtpServerException(exception)

            return matches

        _window_handle, _window_name = \
            self._get_window_handle(window_name)[0:2]
        if not _window_handle:
            raise LdtpServerException('Unable to find window "%s"' % \
                                      window_name)
        appmap = self._get_appmap(_window_handle, _window_name)
        for name in appmap.keys():
            obj = appmap[name]
            # When only role arg is passed
            if role and not child_name and obj['class'] == role:
                matches.append(name)
            # When parent and child_name arg is passed
            if parent and child_name and not role and \
                    self._match_name_to_appmap(parent, obj):
                matches.append(name)
            # When only child_name arg is passed
            if child_name and not role and \
                    self._match_name_to_appmap(child_name, obj):
                return name
                matches.append(name)
            # When role and child_name args are passed
            if role and child_name and obj['class'] == role and \
                    self._match_name_to_appmap(child_name, obj):
                matches.append(name)

        if not matches:
            _name = ''
            _role = ''
            _parent = ''
            if child_name:
                _name = 'name "%s" ' % child_name
            if role:
                _role = 'role "%s" ' % role
            if parent:
                _parent = 'parent "%s"' % parent
            exception = 'Could not find a child %s%s%s' % (_name, _role, _parent)
            raise LdtpServerException(exception)

        return matches