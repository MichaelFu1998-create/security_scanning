def _emit_element(self, element, level, declared_prefixes):
        """"Recursive XML element serializer.

        :Parameters:
            - `element`: the element to serialize
            - `level`: nest level (0 - root element, 1 - stanzas, etc.)
            - `declared_prefixes`: namespace to prefix mapping of already
              declared prefixes.
        :Types:
            - `element`: :etree:`ElementTree.Element`
            - `level`: `int`
            - `declared_prefixes`: `unicode` to `unicode` dictionary

        :Return: serialized element
        :Returntype: `unicode`
        """
        declarations = {}
        declared_prefixes = dict(declared_prefixes)
        name = element.tag
        prefixed = self._make_prefixed(name, True, declared_prefixes,
                                                                declarations)
        start_tag = u"<{0}".format(prefixed)
        end_tag = u"</{0}>".format(prefixed)
        for name, value in element.items():
            prefixed = self._make_prefixed(name, False, declared_prefixes,
                                                                declarations)
            start_tag += u' {0}={1}'.format(prefixed, quoteattr(value))

        declarations = self._make_ns_declarations(declarations,
                                                        declared_prefixes)
        if declarations:
            start_tag += u" " + declarations
        children = []
        for child in element:
            children.append(self._emit_element(child, level +1,
                                                        declared_prefixes))
        if not children and not element.text:
            start_tag += u"/>"
            end_tag = u""
            text = u""
        else:
            start_tag += u">"
            if level > 0 and element.text:
                text = escape(element.text)
            else:
                text = u""
        if level > 1 and element.tail:
            tail = escape(element.tail)
        else:
            tail = u""
        return start_tag + text + u''.join(children) + end_tag + tail