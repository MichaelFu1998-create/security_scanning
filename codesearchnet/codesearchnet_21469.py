def append(self, name, attrs=None, data=None):
        """
        Called when the parser detects a start tag (child element) while in this node. Internally creates an
        :class:`XmlElement` and adds it to the end of this node's children.

        :param name: The tag name to add
        :param attrs: Attributes for the new tag
        :param data: CDATA for the new tag
        :returns: The newly-created element
        :rtype: :class:`XmlElement`
        """
        elem = self.__class__(name, attrs, data, parent=self, index=len(self._children))
        self._children.append(elem)
        return elem