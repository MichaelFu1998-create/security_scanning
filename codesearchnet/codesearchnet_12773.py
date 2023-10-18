def draw(self):
        """
        The master function that is called that draws everything.
        """
        self.ax.set_xlim(-self.plot_radius(), self.plot_radius())
        self.ax.set_ylim(-self.plot_radius(), self.plot_radius())

        self.add_axes_and_nodes()
        self.add_edges()

        self.ax.axis('off')