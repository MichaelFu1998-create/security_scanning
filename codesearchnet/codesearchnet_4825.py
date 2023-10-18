def animate_cluster_allocation(dataset, analyser, animation_velocity = 75, tolerance = 0.1, save_movie = None, title = None):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation on a circle from [0; 2pi].
        
        @param[in] dataset (list): Input data that was used for processing by the network.
        @param[in] analyser (syncnet_analyser): Output dynamic analyser of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] tolerance (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        @param[in] title (string): If it is specified then title will be displayed on the animation plot.
        
        """
        
        figure = plt.figure();
        
        def init_frame():
            return frame_generation(0);
        
        def frame_generation(index_dynamic):
            figure.clf();
            if (title is not None):
                figure.suptitle(title, fontsize = 26, fontweight = 'bold');
            
            ax1 = figure.add_subplot(121, projection='polar');
            
            clusters = analyser.allocate_clusters(eps = tolerance, iteration = index_dynamic);
            dynamic = analyser.output[index_dynamic];
            
            visualizer = cluster_visualizer(size_row = 2);
            visualizer.append_clusters(clusters, dataset);
            
            artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '');
            
            visualizer.show(figure, display = False);
            artist2 = figure.gca();
            
            return [ artist1, artist2 ];
        
        cluster_animation = animation.FuncAnimation(figure, frame_generation, len(analyser), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
#             plt.rcParams['animation.ffmpeg_path'] = 'D:\\Program Files\\ffmpeg-3.3.1-win64-static\\bin\\ffmpeg.exe';
#             ffmpeg_writer = animation.FFMpegWriter(fps = 15);
#             cluster_animation.save(save_movie, writer = ffmpeg_writer);
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();