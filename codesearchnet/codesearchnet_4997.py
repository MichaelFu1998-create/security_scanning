def animate_output_dynamic(sync_output_dynamic, animation_velocity = 75, save_movie = None):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation on a circle from [0; 2pi].
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure();
        
        dynamic = sync_output_dynamic.output[0];
        artist, = plt.polar(dynamic, [1.0] * len(dynamic), 'o', color = 'blue');
        
        def init_frame():
            return [ artist ];
        
        def frame_generation(index_dynamic):
            dynamic = sync_output_dynamic.output[index_dynamic];
            artist.set_data(dynamic, [1.0] * len(dynamic));
            
            return [ artist ];
        
        phase_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
            phase_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();