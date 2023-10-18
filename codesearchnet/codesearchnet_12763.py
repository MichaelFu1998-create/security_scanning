def plot_axis(self, rs, theta):
        """
        Renders the axis.
        """
        xs, ys = get_cartesian(rs, theta)
        self.ax.plot(xs, ys, 'black', alpha=0.3)