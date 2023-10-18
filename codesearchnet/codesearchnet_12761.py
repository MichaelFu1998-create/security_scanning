def plot_radius(self):
        """
        Computes the plot radius: maximum of length of each list of nodes.
        """
        plot_rad = 0
        for group, nodelist in self.nodes.items():
            proposed_radius = len(nodelist) * self.scale
            if proposed_radius > plot_rad:
                plot_rad = proposed_radius
        return plot_rad + self.internal_radius