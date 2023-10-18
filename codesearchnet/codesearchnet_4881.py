def __draw_cluster(self, data, cluster, color, marker):
        """!
        @brief Draw 2-D single cluster on axis using specified color and marker.

        """
        for item in cluster:
            self.__ax.plot(data[item][0], data[item][1], color=color, marker=marker)