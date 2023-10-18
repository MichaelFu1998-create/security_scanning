def emit_stanza(self, element):
        """"Serialize a stanza.

        Must be called after `emit_head`.

        :Parameters:
            - `element`: the element to serialize
        :Types:
            - `element`: :etree:`ElementTree.Element`

        :Return: serialized element
        :Returntype: `unicode`
        """
        if not self._head_emitted:
            raise RuntimeError(".emit_head() must be called first.")
        string = self._emit_element(element, level = 1,
                                    declared_prefixes = self._root_prefixes)
        return remove_evil_characters(string)