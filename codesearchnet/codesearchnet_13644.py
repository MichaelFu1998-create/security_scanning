def as_xml(self):
        """Return the XML error representation.

        :returntype: :etree:`ElementTree.Element`"""
        result = ElementTree.Element(self.error_qname)
        result.append(deepcopy(self.condition))
        if self.text:
            text = ElementTree.SubElement(result, self.text_qname)
            if self.language:
                text.set(XML_LANG_QNAME, self.language)
            text.text = self.text
        return result