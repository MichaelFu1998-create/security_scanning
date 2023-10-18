def _split_qname(self, name, is_element):
        """Split an element of attribute qname into namespace and local
        name.

        :Parameters:
            - `name`: element or attribute QName
            - `is_element`: `True` for an element, `False` for an attribute
        :Types:
            - `name`: `unicode`
            - `is_element`: `bool`

        :Return: namespace URI, local name
        :returntype: `unicode`, `unicode`"""
        if name.startswith(u"{"):
            namespace, name = name[1:].split(u"}", 1)
            if namespace in STANZA_NAMESPACES:
                namespace = self.stanza_namespace
        elif is_element:
            raise ValueError(u"Element with no namespace: {0!r}".format(name))
        else:
            namespace = None
        return namespace, name