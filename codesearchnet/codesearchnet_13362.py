def as_xml(self):
        """Return the XML stanza representation.

        Always return an independent copy of the stanza XML representation,
        which can be freely modified without affecting the stanza.

        :returntype: :etree:`ElementTree.Element`"""
        result = Stanza.as_xml(self)
        if self._subject:
            child = ElementTree.SubElement(result, self._subject_tag)
            child.text = self._subject
        if self._body:
            child = ElementTree.SubElement(result, self._body_tag)
            child.text = self._body
        if self._thread:
            child = ElementTree.SubElement(result, self._thread_tag)
            child.text = self._thread
        return result