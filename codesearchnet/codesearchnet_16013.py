def _xml(self, root):
        """
        Return an XML element representing this element
        """
        element = root.createElement(self.name)

        # Add attributes
        keys = self.attrs.keys()
        keys.sort()
        for a in keys:
            element.setAttribute(a, self.attrs[a])

        if self.body:
            text = root.createTextNode(self.body)
            element.appendChild(text)

        for c in self.elements:
            element.appendChild(c._xml(root))

        return element