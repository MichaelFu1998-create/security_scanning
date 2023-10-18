def __draw_canvas_cluster(self, ax, dimension, cluster_descr):
        """!
        @brief Draw canvas cluster descriptor.

        @param[in] ax (Axis): Axis of the canvas where canvas cluster descriptor should be displayed.
        @param[in] dimension (uint): Canvas dimension.
        @param[in] cluster_descr (canvas_cluster_descr): Canvas cluster descriptor that should be displayed.

        @return (fig) Figure where clusters are shown.

        """

        cluster = cluster_descr.cluster
        data = cluster_descr.data
        marker = cluster_descr.marker
        markersize = cluster_descr.markersize
        color = cluster_descr.color
        
        for item in cluster:
            if dimension == 1:
                if data is None:
                    ax.plot(item[0], 0.0, color = color, marker = marker, markersize = markersize)
                else:
                    ax.plot(data[item][0], 0.0, color = color, marker = marker, markersize = markersize)

            elif dimension == 2:
                if data is None:
                    ax.plot(item[0], item[1], color = color, marker = marker, markersize = markersize)
                else:
                    ax.plot(data[item][0], data[item][1], color = color, marker = marker, markersize = markersize)
        
            elif dimension == 3:
                if data is None:
                    ax.scatter(item[0], item[1], item[2], c = color, marker = marker, s = markersize)
                else:
                    ax.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker, s = markersize)