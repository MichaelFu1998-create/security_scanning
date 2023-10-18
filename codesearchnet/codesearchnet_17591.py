def add_assay(self, name, assay):
        """
        Add an assay to the material.

        :param name:  Assay name.
        :param assay: Numpy array containing the compound mass fractions for
          the assay. The sequence of the assay's elements must correspond to
          the sequence of the material's compounds.
        """

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.compound_count,):
            raise Exception("Invalid assay: It must have the same number of "
                            "elements as the material has compounds.")
        elif name in self.raw_assays.keys():
            raise Exception("Invalid assay: An assay with that name already "
                            "exists.")
        self.raw_assays[name] = assay
        self.converted_assays[name] = assay