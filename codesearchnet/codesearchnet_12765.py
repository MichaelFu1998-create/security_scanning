def group_theta(self, group):
        """
        Computes the theta along which a group's nodes are aligned.
        """
        for i, g in enumerate(self.nodes.keys()):
            if g == group:
                break

        return i * self.major_angle