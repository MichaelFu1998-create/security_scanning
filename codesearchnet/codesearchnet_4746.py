def animate_cluster_allocation(data, observer, animation_velocity=75, movie_fps=5, save_movie=None):
        """!
        @brief Animate clustering process of genetic clustering algorithm.
        @details This method can be also used for rendering movie of clustering process and 'ffmpeg' is required for that purpuse.
        
        @param[in] data (list): Input data that was used for clustering process by the algorithm.
        @param[in] observer (ga_observer): Observer that was used for collection information about clustering process.
                    Be sure that whole information was collected by the observer.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure()
        
        def init_frame():
            return frame_generation(0)

        def frame_generation(index_iteration):
            figure.clf()
            
            figure.suptitle("Clustering genetic algorithm (iteration: " + str(index_iteration) + ")", fontsize=18, fontweight='bold')
            
            visualizer = cluster_visualizer(4, 2, ["The best pop. on step #" + str(index_iteration), "The best population"])
            
            local_minimum_clusters = ga_math.get_clusters_representation(observer.get_population_best()['chromosome'][index_iteration])
            visualizer.append_clusters(local_minimum_clusters, data, 0)
            
            global_minimum_clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][index_iteration])
            visualizer.append_clusters(global_minimum_clusters, data, 1)
            
            ax1 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            ga_visualizer.show_evolution(observer, 0, index_iteration + 1, ax1, False)
            
            visualizer.show(figure, shift=0, display=False)
            figure.subplots_adjust(top=0.85)
            
            return [figure.gca()]
        
        iterations = len(observer)
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval=animation_velocity, init_func=init_frame, repeat_delay=5000)

        if save_movie is not None:
            cluster_animation.save(save_movie, writer='ffmpeg', fps=movie_fps, bitrate=1500)
        else:
            plt.show()