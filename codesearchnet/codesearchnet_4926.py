def show_clusters(sample, clusters, centers, initial_centers = None, **kwargs):
        """!
        @brief Display K-Means clustering results.
        
        @param[in] sample (list): Dataset that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] centers (array_like): Centers that were allocated by the algorithm.
        @param[in] initial_centers (array_like): Initial centers that were used by the algorithm, if 'None' then initial centers are not displyed.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'figure', 'display', 'offset').
        
        <b>Keyword Args:</b><br>
            - figure (figure): If 'None' then new is figure is created, otherwise specified figure is used for visualization.
            - display (bool): If 'True' then figure will be shown by the method, otherwise it should be shown manually using matplotlib function 'plt.show()'.
            - offset (uint): Specify axes index on the figure where results should be drawn (only if argument 'figure' is specified).
        
        @return (figure) Figure where clusters were drawn.
        
        """

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        
        offset = kwargs.get('offset', 0)
        figure = kwargs.get('figure', None)
        display = kwargs.get('display', True)

        if figure is None:
            figure = visualizer.show(display = False)
        else:
            visualizer.show(figure = figure, display = False)
        
        kmeans_visualizer.__draw_centers(figure, offset, visualizer, centers, initial_centers)
        kmeans_visualizer.__draw_rays(figure, offset, visualizer, sample, clusters, centers)
        
        if display is True:
            plt.show()

        return figure