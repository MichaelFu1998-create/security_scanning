def prepare(self):
        """Prepare the date in the instance state for serialization.
        """

        # Create a collection for the attributes and elements of
        # this instance.
        attributes, elements = OrderedDict(), []

        # Initialize the namespace map.
        nsmap = dict([self.meta.namespace])

        # Iterate through all declared items.
        for name, item in self._items.items():
            if isinstance(item, Attribute):
                # Prepare the item as an attribute.
                attributes[name] = item.prepare(self)

            elif isinstance(item, Element):
                # Update the nsmap.
                nsmap.update([item.namespace])

                # Prepare the item as an element.
                elements.append(item)

        # Return the collected attributes and elements
        return attributes, elements, nsmap