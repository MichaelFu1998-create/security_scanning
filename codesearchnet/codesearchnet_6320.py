def weight(self):
        """Calculate the mol mass of the compound

        Returns
        -------
        float
            the mol mass
        """
        try:
            return sum([count * elements_and_molecular_weights[element]
                        for element, count in self.elements.items()])
        except KeyError as e:
            warn("The element %s does not appear in the periodic table" % e)