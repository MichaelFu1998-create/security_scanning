def animate_pattern_recognition(syncpr_output_dynamic, image_height, image_width, animation_velocity = 75, title = None, save_movie = None):
        """!
        @brief Shows animation of pattern recognition process that has been preformed by the oscillatory network.
        
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] title (string): Title of the animation that is displayed on a figure if it is specified.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        figure = plt.figure();
        
        def init_frame():
            return frame_generation(0);
        
        def frame_generation(index_dynamic):
            figure.clf();
            
            if (title is not None):
                figure.suptitle(title, fontsize = 26, fontweight = 'bold')
            
            ax1 = figure.add_subplot(121, projection='polar');
            ax2 = figure.add_subplot(122);
            
            dynamic = syncpr_output_dynamic.output[index_dynamic];
            
            artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '');
            artist2 = syncpr_visualizer.__show_pattern(ax2, syncpr_output_dynamic, image_height, image_width, index_dynamic);
            
            return [ artist1, artist2 ];
        
        cluster_animation = animation.FuncAnimation(figure, frame_generation, len(syncpr_output_dynamic), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
#             plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\annoviko\\programs\\ffmpeg-win64-static\\bin\\ffmpeg.exe';
#             ffmpeg_writer = animation.FFMpegWriter();
#             cluster_animation.save(save_movie, writer = ffmpeg_writer, fps = 15);
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();