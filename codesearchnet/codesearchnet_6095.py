def get_properties(self, mode, name_list=None):
        """Return properties as list of 2-tuples (name, value).

        If mode is 'name', then None is returned for the value.

        name
            the property name in Clark notation.
        value
            may have different types, depending on the status:
            - string or unicode: for standard property values.
            - etree.Element: for complex values.
            - DAVError in case of errors.
            - None: if mode == 'name'.

        @param mode: "allprop", "name", or "named"
        @param name_list: list of property names in Clark Notation (required for mode 'named')

        This default implementation basically calls self.get_property_names() to
        get the list of names, then call self.get_property_value on each of them.
        """
        assert mode in ("allprop", "name", "named")

        if mode in ("allprop", "name"):
            # TODO: 'allprop' could have nameList, when <include> option is
            # implemented
            assert name_list is None
            name_list = self.get_property_names(mode == "allprop")
        else:
            assert name_list is not None

        propList = []
        namesOnly = mode == "name"
        for name in name_list:
            try:
                if namesOnly:
                    propList.append((name, None))
                else:
                    value = self.get_property_value(name)
                    propList.append((name, value))
            except DAVError as e:
                propList.append((name, e))
            except Exception as e:
                propList.append((name, as_DAVError(e)))
                if self.provider.verbose >= 2:
                    traceback.print_exc(10, sys.stdout)

        return propList