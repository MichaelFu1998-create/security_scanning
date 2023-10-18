def add_assay(self, name, solid_density, H2O_fraction, assay):
        """Add an assay to the material.

        :param name: The name of the new assay.
        :param assay: A numpy array containing the size class mass fractions
          for the assay. The sequence of the assay's elements must correspond
          to the sequence of the material's size classes.
        """

        if not type(solid_density) is float:
            raise Exception("Invalid solid density. It must be a float.")
        self.solid_densities[name] = solid_density

        if not type(H2O_fraction) is float:
            raise Exception("Invalid H2O fraction. It must be a float.")
        self.H2O_fractions[name] = H2O_fraction

        if not type(assay) is numpy.ndarray:
            raise Exception("Invalid assay. It must be a numpy array.")
        elif not assay.shape == (self.size_class_count,):
            raise Exception(
                "Invalid assay: It must have the same number of elements as "
                "the material has size classes.")
        elif name in self.assays.keys():
            raise Exception(
                "Invalid assay: An assay with that name already exists.")
        self.assays[name] = assay