def animate_correlation_matrix(sync_output_dynamic, animation_velocity = 75, colormap = 'cool', save_movie = None):
        """!
        @brief Shows animation of correlation matrix between oscillators during simulation.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] colormap (string): Name of colormap that is used by matplotlib ('gray', 'pink', 'cool', spring', etc.).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure()
        
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(0)
        artist = plt.imshow(correlation_matrix, cmap = plt.get_cmap(colormap), interpolation='kaiser', vmin = 0.0, vmax = 1.0)
        
        def init_frame(): 
            return [ artist ]
        
        def frame_generation(index_dynamic):
            correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(index_dynamic)
            artist.set_data(correlation_matrix)
            
            return [ artist ]

        correlation_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), init_func = init_frame, interval = animation_velocity , repeat_delay = 1000, blit = True)
        
        if (save_movie is not None):
            correlation_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500)
        else:
            plt.show()