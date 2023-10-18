def animate_spike_ensembles(pcnn_output_dynamic, image_size):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        @param[in] image_size (tuple): Image size represented as (height, width).
        
        """
        
        figure = plt.figure()
        
        time_signal = pcnn_output_dynamic.allocate_time_signal()
        spike_ensembles = pcnn_output_dynamic.allocate_spike_ensembles()
        
        spike_animation = []
        ensemble_index = 0
        for t in range(len(time_signal)):
            image_color_segments = [(255, 255, 255)] * (image_size[0] * image_size[1])
            
            if time_signal[t] > 0:
                for index_pixel in spike_ensembles[ensemble_index]:
                    image_color_segments[index_pixel] = (0, 0, 0)
                
                ensemble_index += 1

            stage = numpy.array(image_color_segments, numpy.uint8)
            stage = numpy.reshape(stage, image_size + ((3),)) # ((3),) it's size of RGB - third dimension.
            image_cluster = Image.fromarray(stage, 'RGB')
            
            spike_animation.append( [ plt.imshow(image_cluster, interpolation='none') ] )
            
        
        im_ani = animation.ArtistAnimation(figure, spike_animation, interval=75, repeat_delay=3000, blit=True)
        plt.show()