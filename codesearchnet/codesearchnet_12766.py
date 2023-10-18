def add_axes_and_nodes(self):
        """
        Adds the axes (i.e. 2 or 3 axes, not to be confused with matplotlib
        axes) and the nodes that belong to each axis.
        """
        for i, (group, nodelist) in enumerate(self.nodes.items()):
            theta = self.group_theta(group)

            if self.has_edge_within_group(group):
                    theta = theta - self.minor_angle
                    self.plot_nodes(nodelist, theta, group)

                    theta = theta + 2 * self.minor_angle
                    self.plot_nodes(nodelist, theta, group)

            else:
                self.plot_nodes(nodelist, theta, group)