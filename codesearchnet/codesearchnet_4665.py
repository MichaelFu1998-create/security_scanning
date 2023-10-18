def __create_canvas(self, dimension, pairs, position, **kwargs):
        """!
        @brief Create new canvas with user defined parameters to display cluster or chunk of cluster on it.

        @param[in] dimension (uint): Data-space dimension.
        @param[in] pairs (list): Pair of coordinates that will be displayed on the canvas. If empty than label will not
                    be displayed on the canvas.
        @param[in] position (uint): Index position of canvas on a grid.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'visible_axis' 'visible_labels', 'visible_grid').

        <b>Keyword Args:</b><br>
            - visible_axis (bool): Defines visibility of axes on each canvas, if True - axes are visible.
               By default axis are not displayed.
            - visible_labels (bool): Defines visibility of labels on each canvas, if True - labels is displayed.
               By default labels are displayed.
            - visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
               By default grid is displayed.

        @return (matplotlib.Axis) Canvas to display cluster of chuck of cluster.

        """
        visible_grid = kwargs.get('visible_grid', True)
        visible_labels = kwargs.get('visible_labels', True)
        visible_axis = kwargs.get('visible_axis', False)

        ax = self.__figure.add_subplot(self.__grid_spec[position])

        if dimension > 1:
            if visible_labels:
                ax.set_xlabel("x%d" % pairs[position][0])
                ax.set_ylabel("x%d" % pairs[position][1])
        else:
            ax.set_ylim(-0.5, 0.5)
            ax.set_yticklabels([])

        if visible_grid:
            ax.grid(True)

        if not visible_axis:
            ax.set_yticklabels([])
            ax.set_xticklabels([])

        return ax