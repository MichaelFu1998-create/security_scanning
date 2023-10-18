def initialize_minor_angle(self):
        """
        Computes the minor angle: 2pi radians / 3 * number of groups.
        """
        num_groups = len(self.nodes.keys())

        self.minor_angle = 2 * np.pi / (6 * num_groups)