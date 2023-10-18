def add_assay(self, name, assay):
        """
        Add an assay to the material.

        :param name: The name of the new assay.
        :param assay: A list containing the compound mass fractions for
          the assay. The sequence of the assay's elements must correspond to
          the sequence of the material's compounds.
        """

        if not type(assay) is list:
            raise Exception('Invalid assay. It must be a list.')

        elif not len(assay) == self.compound_count:
            raise Exception('Invalid assay: It must have the same number of '
                            'elements as the material has compounds.')

        elif name in self.assays:
            raise Exception('Invalid assay: An assay with that name already '
                            'exists.')

        self.assays[name] = assay