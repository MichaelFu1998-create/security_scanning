def add_prefix(self, namespace, prefix):
        """Add a new namespace prefix.

        If the root element has not yet been emitted the prefix will
        be declared there, otherwise the prefix will be declared on the
        top-most element using this namespace in every stanza.

        :Parameters:
            - `namespace`: the namespace URI
            - `prefix`: the prefix string
        :Types:
            - `namespace`: `unicode`
            - `prefix`: `unicode`
        """
        if prefix == "xml" and namespace != XML_NS:
            raise ValueError, "Cannot change 'xml' prefix meaning"
        self._prefixes[namespace] = prefix