def animate(sync_output_dynamic, title = None, save_movie = None):
        """!
        @brief Shows animation of phase coordinates and animation of correlation matrix together for the Sync dynamic output on the same figure.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] title (string): Title of the animation that is displayed on a figure if it is specified.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        dynamic = sync_output_dynamic.output[0];
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(0);
        
        figure = plt.figure(1);
        if (title is not None):
            figure.suptitle(title, fontsize = 26, fontweight = 'bold')
        
        ax1 = figure.add_subplot(121, projection='polar');
        ax2 = figure.add_subplot(122);
        
        artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '');
        artist2 = ax2.imshow(correlation_matrix, cmap = plt.get_cmap('Accent'), interpolation='kaiser');
        
        def init_frame():
            return [ artist1, artist2 ];

        def frame_generation(index_dynamic):
            dynamic = sync_output_dynamic.output[index_dynamic];
            artist1.set_data(dynamic, [1.0] * len(dynamic));
            
            correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(index_dynamic);
            artist2.set_data(correlation_matrix);
            
            return [ artist1, artist2 ];
        
        dynamic_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), interval = 75, init_func = init_frame, repeat_delay = 5000);
        
        if (save_movie is not None):
            dynamic_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();