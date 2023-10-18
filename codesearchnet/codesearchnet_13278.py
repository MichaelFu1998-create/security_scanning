def as_xml(self, parent = None):
        """Make an XML element from self.

        :Parameters:
            - `parent`: Parent element
        :Types:
            - `parent`: :etree:`ElementTree.Element`
        """
        if parent is not None:
            element = ElementTree.SubElement(parent, ITEM_TAG)
        else:
            element = ElementTree.Element(ITEM_TAG)
        element.set("jid", unicode(self.jid))
        if self.name is not None:
            element.set("name", self.name)
        if self.subscription is not None:
            element.set("subscription", self.subscription)
        if self.ask:
            element.set("ask", self.ask)
        if self.approved:
            element.set("approved", "true")
        for group in self.groups:
            ElementTree.SubElement(element, GROUP_TAG).text = group
        return element