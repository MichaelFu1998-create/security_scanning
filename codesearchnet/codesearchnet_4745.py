def show_clusters(data, observer, marker='.', markersize=None):
        """!
        @brief Shows allocated clusters by the genetic algorithm.
        
        @param[in] data (list): Input data that was used for clustering process by the algorithm.
        @param[in] observer (ga_observer): Observer that was used for collection information about clustering process.
        @param[in] marker (char): Type of marker that should be used for object (point) representation.
        @param[in] markersize (uint): Size of the marker that is used for object (point) representation.
        
        @note If you have clusters instead of observer then 'cluster_visualizer' can be used for visualization purposes.
        
        @see cluster_visualizer
        
        """
        
        figure = plt.figure()
        ax1 = figure.add_subplot(121)
        
        clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][-1])
        
        visualizer = cluster_visualizer(1, 2)
        visualizer.append_clusters(clusters, data, 0, marker, markersize)
        visualizer.show(figure, display=False)
        
        ga_visualizer.show_evolution(observer, 0, None, ax1, True)