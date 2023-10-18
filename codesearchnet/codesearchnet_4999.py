def animate_phase_matrix(sync_output_dynamic, grid_width = None, grid_height = None, animation_velocity = 75, colormap = 'jet', save_movie = None):
        """!
        @brief Shows animation of phase matrix between oscillators during simulation on 2D stage.
        @details If grid_width or grid_height are not specified than phase matrix size will by calculated automatically by square root.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] grid_width (uint): Width of the phase matrix.
        @param[in] grid_height (uint): Height of the phase matrix.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] colormap (string): Name of colormap that is used by matplotlib ('gray', 'pink', 'cool', spring', etc.).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure();
        
        def init_frame(): 
            return frame_generation(0);
        
        def frame_generation(index_dynamic):
            figure.clf();
            axis = figure.add_subplot(111);
            
            phase_matrix = sync_output_dynamic.allocate_phase_matrix(grid_width, grid_height, index_dynamic);
            axis.imshow(phase_matrix, cmap = plt.get_cmap(colormap), interpolation='kaiser', vmin = 0.0, vmax = 2.0 * math.pi);
            artist = figure.gca();
            
            return [ artist ];

        phase_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), init_func = init_frame, interval = animation_velocity , repeat_delay = 1000);
        
        if (save_movie is not None):
            phase_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();