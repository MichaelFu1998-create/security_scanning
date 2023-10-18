def __draw_canvas_cluster(self, axis_storage, cluster_descr, pairs):
        """!
        @brief Draw clusters.

        @param[in] axis_storage (list): List of matplotlib axis where cluster dimensional chunks are displayed.
        @param[in] cluster_descr (canvas_cluster_descr): Canvas cluster descriptor that should be displayed.
        @param[in] pairs (list): List of coordinates that should be displayed.

        """

        for index_axis in range(len(axis_storage)):
            for item in cluster_descr.cluster:
                if len(pairs) > 0:
                    self.__draw_cluster_item_multi_dimension(axis_storage[index_axis], pairs[index_axis], item, cluster_descr)
                else:
                    self.__draw_cluster_item_one_dimension(axis_storage[index_axis], item, cluster_descr)