def animate_cluster_allocation(data, observer, animation_velocity = 500, movie_fps = 1, save_movie = None):
        """!
        @brief Animates clustering process that is performed by K-Means algorithm.

        @param[in] data (list): Dataset that is used for clustering.
        @param[in] observer (kmeans_observer): EM observer that was used for collection information about clustering process.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.

        """
        figure = plt.figure()

        def init_frame():
            return frame_generation(0)

        def frame_generation(index_iteration):
            figure.clf()

            figure.suptitle("K-Means algorithm (iteration: " + str(index_iteration) + ")", fontsize=18, fontweight='bold')

            clusters = observer.get_clusters(index_iteration)
            centers = observer.get_centers(index_iteration)
            kmeans_visualizer.show_clusters(data, clusters, centers, None, figure=figure, display=False)

            figure.subplots_adjust(top=0.85)

            return [figure.gca()]

        iterations = len(observer)
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval=animation_velocity,
                                                    init_func=init_frame, repeat_delay=5000)

        if save_movie is not None:
            cluster_animation.save(save_movie, writer='ffmpeg', fps=movie_fps, bitrate=3000)
        else:
            plt.show()