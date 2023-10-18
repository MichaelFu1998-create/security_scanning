def _create_element_list(self):
        """
        Extract an alphabetically sorted list of elements from the
        material's compounds.

        :returns: Alphabetically sorted list of elements.
        """

        element_set = stoich.elements(self.compounds)
        return sorted(list(element_set))