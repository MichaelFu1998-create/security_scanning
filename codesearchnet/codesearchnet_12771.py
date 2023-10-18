def draw_edge(self, n1, n2, d, group):
        """
        Renders the given edge (n1, n2) to the plot.
        """
        start_radius = self.node_radius(n1)
        start_theta = self.node_theta(n1)

        end_radius = self.node_radius(n2)
        end_theta = self.node_theta(n2)

        start_theta, end_theta = self.correct_angles(start_theta, end_theta)
        start_theta, end_theta = self.adjust_angles(n1, start_theta, n2,
                                                    end_theta)

        middle1_radius = np.min([start_radius, end_radius])
        middle2_radius = np.max([start_radius, end_radius])

        if start_radius > end_radius:
            middle1_radius, middle2_radius = middle2_radius, middle1_radius

        middle1_theta = np.mean([start_theta, end_theta])
        middle2_theta = np.mean([start_theta, end_theta])

        startx, starty = get_cartesian(start_radius, start_theta)
        middle1x, middle1y = get_cartesian(middle1_radius, middle1_theta)
        middle2x, middle2y = get_cartesian(middle2_radius, middle2_theta)
        # middlex, middley = get_cartesian(middle_radius, middle_theta)
        endx, endy = get_cartesian(end_radius, end_theta)

        verts = [(startx, starty),
                 (middle1x, middle1y),
                 (middle2x, middle2y),
                 (endx, endy)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]

        path = Path(verts, codes)
        if self.edge_colormap is None:
            edgecolor = 'black'
        else:
            edgecolor = self.edge_colormap[group]
        patch = patches.PathPatch(path, lw=self.linewidth, facecolor='none',
                                  edgecolor=edgecolor, alpha=0.3)
        self.ax.add_patch(patch)