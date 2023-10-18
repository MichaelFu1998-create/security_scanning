def __draw_cluster_item_one_dimension(self, ax, item, cluster_descr):
        """!
        @brief Draw cluster point in one dimensional data space..

        @param[in] ax (axis): Matplotlib axis that is used to display chunk of cluster point.
        @param[in] item (list): Data point or index of data point.
        @param[in] cluster_descr (canvas_cluster_descr): Cluster description whose point is visualized.

        """

        if cluster_descr.data is None:
            ax.plot(item[0], 0.0,
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)
        else:
            ax.plot(cluster_descr.data[item][0], 0.0,
                    color=cluster_descr.color, marker=cluster_descr.marker, markersize=cluster_descr.markersize)