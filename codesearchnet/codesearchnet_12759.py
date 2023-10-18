def initialize_major_angle(self):
        """
        Computes the major angle: 2pi radians / number of groups.
        """
        num_groups = len(self.nodes.keys())
        self.major_angle = 2 * np.pi / num_groups