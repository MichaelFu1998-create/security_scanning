def plot_nodes(self, nodelist, theta, group):
        """
        Plots nodes to screen.
        """
        for i, node in enumerate(nodelist):
            r = self.internal_radius + i * self.scale
            x, y = get_cartesian(r, theta)
            circle = plt.Circle(xy=(x, y), radius=self.dot_radius,
                                color=self.node_colormap[group], linewidth=0)
            self.ax.add_patch(circle)