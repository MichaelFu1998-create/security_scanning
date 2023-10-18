def show_clusters(sample, clusters, representatives, **kwargs):
        """!
        @brief Display BSAS clustering results.

        @param[in] sample (list): Dataset that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] representatives (array_like): Allocated representatives correspond to clusters.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'figure', 'display', 'offset').

        <b>Keyword Args:</b><br>
            - figure (figure): If 'None' then new is figure is created, otherwise specified figure is used for visualization.
            - display (bool): If 'True' then figure will be shown by the method, otherwise it should be shown manually using matplotlib function 'plt.show()'.
            - offset (uint): Specify axes index on the figure where results should be drawn (only if argument 'figure' is specified).

        @return (figure) Figure where clusters were drawn.

        """

        figure = kwargs.get('figure', None)
        display = kwargs.get('display', True)
        offset = kwargs.get('offset', 0)

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, canvas=offset)

        for cluster_index in range(len(clusters)):
            visualizer.append_cluster_attribute(offset, cluster_index, [representatives[cluster_index]], '*', 10)

        return visualizer.show(figure=figure, display=display)