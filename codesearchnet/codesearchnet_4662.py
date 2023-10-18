def show(self, pair_filter=None, **kwargs):
        """!
        @brief Shows clusters (visualize) in multi-dimensional space.

        @param[in] pair_filter (list): List of coordinate pairs that should be displayed. This argument is used as a filter.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'visible_axis' 'visible_labels', 'visible_grid', 'row_size').

        <b>Keyword Args:</b><br>
            - visible_axis (bool): Defines visibility of axes on each canvas, if True - axes are visible.
               By default axis of each canvas are not displayed.
            - visible_labels (bool): Defines visibility of labels on each canvas, if True - labels is displayed.
               By default labels of each canvas are displayed.
            - visible_grid (bool): Defines visibility of grid on each canvas, if True - grid is displayed.
               By default grid of each canvas is displayed.
            - max_row_size (uint): Maximum number of canvases on one row.

        """

        if not len(self.__clusters) > 0:
            raise ValueError("There is no non-empty clusters for visualization.")

        cluster_data = self.__clusters[0].data or self.__clusters[0].cluster
        dimension = len(cluster_data[0])

        acceptable_pairs = pair_filter or []
        pairs = []
        amount_axis = 1
        axis_storage = []

        if dimension > 1:
            pairs = self.__create_pairs(dimension, acceptable_pairs)
            amount_axis = len(pairs)

        self.__figure = plt.figure()
        self.__grid_spec = self.__create_grid_spec(amount_axis, kwargs.get('max_row_size', 4))

        for index in range(amount_axis):
            ax = self.__create_canvas(dimension, pairs, index, **kwargs)
            axis_storage.append(ax)

        for cluster_descr in self.__clusters:
            self.__draw_canvas_cluster(axis_storage, cluster_descr, pairs)

        plt.show()