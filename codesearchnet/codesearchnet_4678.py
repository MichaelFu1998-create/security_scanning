def show_clusters(clusters, sample, covariances, means, figure = None, display = True):
        """!
        @brief Draws clusters and in case of two-dimensional dataset draws their ellipses.
        
        @param[in] clusters (list): Clusters that were allocated by the algorithm.
        @param[in] sample (list): Dataset that were used for clustering.
        @param[in] covariances (list): Covariances of the clusters.
        @param[in] means (list): Means of the clusters.
        @param[in] figure (figure): If 'None' then new is figure is creater, otherwise specified figure is used
                    for visualization.
        @param[in] display (bool): If 'True' then figure will be shown by the method, otherwise it should be
                    shown manually using matplotlib function 'plt.show()'.
        
        @return (figure) Figure where clusters were drawn.
        
        """
        
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        
        if figure is None:
            figure = visualizer.show(display = False)
        else:
            visualizer.show(figure = figure, display = False)
        
        if len(sample[0]) == 2:
            ema_visualizer.__draw_ellipses(figure, visualizer, clusters, covariances, means)

        if display is True:
            plt.show()

        return figure