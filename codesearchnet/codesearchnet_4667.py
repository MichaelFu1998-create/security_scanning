def __draw_cluster_item_multi_dimension(self, ax, pair, item, cluster_descr):
        """!
        @brief Draw cluster chunk defined by pair coordinates in data space with dimension greater than 1.

        @param[in] ax (axis): Matplotlib axis that is used to display chunk of cluster point.
        @param[in] pair (list): Coordinate of the point that should be displayed.
        @param[in] item (list): Data point or index of data point.
        @param[in] cluster_descr (canvas_cluster_descr): Cluster description whose point is visualized.

        """

        index_dimension1 = pair[0]
        index_dimension2 = pair[1]

        if cluster_descr.data is None:
            ax.plot(item[index_dimension1], item[index_dimension2],
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)
        else:
            ax.plot(cluster_descr.data[item][index_dimension1], cluster_descr.data[item][index_dimension2],
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)