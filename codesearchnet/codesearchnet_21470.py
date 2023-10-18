def insert(self, before, name, attrs=None, data=None):
        """
        Inserts a new element as a child of this element, before the specified index or sibling.

        :param before: An :class:`XmlElement` or a numeric index to insert the new node before
        :param name: The tag name to add
        :param attrs: Attributes for the new tag
        :param data: CDATA for the new tag
        :returns: The newly-created element
        :rtype: :class:`XmlElement`
        """
        if isinstance(before, self.__class__):
            if before.parent != self:
                raise ValueError('Cannot insert before an element with a different parent.')
            before = before.index
        # Make sure 0 <= before <= len(_children).
        before = min(max(0, before), len(self._children))
        elem = self.__class__(name, attrs, data, parent=self, index=before)
        self._children.insert(before, elem)
        # Re-index all the children.
        for idx, c in enumerate(self._children):
            c.index = idx
        return elem