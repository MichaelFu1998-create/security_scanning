def clear(self):
        """
        Set all the size class masses and H20_mass in the package to zero
        and the solid_density to 1.0
        """

        self.solid_density = 1.0
        self.H2O_mass = 0.0
        self.size_class_masses = self.size_class_masses * 0.0