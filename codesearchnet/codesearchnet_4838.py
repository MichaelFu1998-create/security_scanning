def __draw_two_dimension_data(ax, data, pair):
        """!
        @brief Display data in two-dimensional canvas.

        @param[in] ax (Axis): Canvas where data should be displayed.
        @param[in] data (list): Data points that should be displayed.
        @param[in] pair (tuple): Pair of dimension indexes.

        """
        ax.set_xlabel("x%d" % pair[0])
        ax.set_ylabel("x%d" % pair[1])

        for point in data:
            if len(data[0]) > 1:
                ax.plot(point[pair[0]], point[pair[1]], color='red', marker='.')
            else:
                ax.plot(point[pair[0]], 0, color='red', marker='.')
                ax.yaxis.set_ticklabels([])