def _create_element_list_(self):
        """
        Extract an alphabetically sorted list of elements from the compounds of
        the material.

        :returns: An alphabetically sorted list of elements.
        """

        element_set = stoich.elements(self.compounds)
        return sorted(list(element_set))