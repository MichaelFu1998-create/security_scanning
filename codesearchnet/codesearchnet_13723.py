def as_xml(self):
        """Return the XML stanza representation.

        Always return an independent copy of the stanza XML representation,
        which can be freely modified without affecting the stanza.

        :returntype: :etree:`ElementTree.Element`"""
        result = Stanza.as_xml(self)
        if self._show:
            child = ElementTree.SubElement(result, self._show_tag)
            child.text = self._show
        if self._status:
            child = ElementTree.SubElement(result, self._status_tag)
            child.text = self._status
        if self._priority:
            child = ElementTree.SubElement(result, self._priority_tag)
            child.text = unicode(self._priority)
        return result