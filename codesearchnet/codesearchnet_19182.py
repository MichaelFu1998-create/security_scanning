def set_inherited_traits(self, egg_donor, sperm_donor):
        """Accept either strings or Gods as inputs."""
        if type(egg_donor) == str:
            self.reproduce_asexually(egg_donor, sperm_donor)
        else:
            self.reproduce_sexually(egg_donor, sperm_donor)