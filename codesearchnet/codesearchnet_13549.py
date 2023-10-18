def _make_prefixed(self, name, is_element, declared_prefixes, declarations):
        """Return namespace-prefixed tag or attribute name.

        Add appropriate declaration to `declarations` when neccessary.

        If no prefix for an element namespace is defined, make the elements
        namespace default (no prefix). For attributes, make up a prefix in such
        case.

        :Parameters:
            - `name`: QName ('{namespace-uri}local-name')
              to convert
            - `is_element`: `True` for element, `False` for an attribute
            - `declared_prefixes`: mapping of prefixes already declared
              at this scope
            - `declarations`: XMLNS declarations on the current element.
        :Types:
            - `name`: `unicode`
            - `is_element`: `bool`
            - `declared_prefixes`: `unicode` to `unicode` dictionary
            - `declarations`: `unicode` to `unicode` dictionary

        :Returntype: `unicode`"""
        namespace, name = self._split_qname(name, is_element)
        if namespace is None:
            prefix = None
        elif namespace in declared_prefixes:
            prefix = declared_prefixes[namespace]
        elif namespace in self._prefixes:
            prefix = self._prefixes[namespace]
            declarations[namespace] = prefix
            declared_prefixes[namespace] = prefix
        else:
            if is_element:
                prefix = None
            else:
                prefix = self._make_prefix(declared_prefixes)
            declarations[namespace] = prefix
            declared_prefixes[namespace] = prefix
        if prefix:
            return prefix + u":" + name
        else:
            return name