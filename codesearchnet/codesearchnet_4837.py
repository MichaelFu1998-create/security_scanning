def show_clusters(data, clusters, noise=None):
        """!
        @brief Display CLIQUE clustering results.

        @param[in] data (list): Data that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] noise (array_like): Noise that were allocated by the algorithm.

        """
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, data)
        visualizer.append_cluster(noise or [], data, marker='x')
        visualizer.show()