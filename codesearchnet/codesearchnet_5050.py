def __show_pattern(ax_handle, syncpr_output_dynamic, image_height, image_width, iteration):
        """!
        @brief Draws pattern on specified ax.
        
        @param[in] ax_handle (Axis): Axis where pattern should be drawn.
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        @param[in] iteration (uint): Simulation iteration that should be used for extracting pattern.
        
        @return (matplotlib.artist) Artist (pattern) that is rendered in the canvas.
        
        """
        
        current_dynamic = syncpr_output_dynamic.output[iteration];
        stage_picture = [(255, 255, 255)] * (image_height * image_width);
        for index_phase in range(len(current_dynamic)):
            phase = current_dynamic[index_phase];
            
            pixel_color = math.floor( phase * (255 / (2 * math.pi)) );
            stage_picture[index_phase] = (pixel_color, pixel_color, pixel_color);
          
        stage = numpy.array(stage_picture, numpy.uint8);
        stage = numpy.reshape(stage, (image_height, image_width) + ((3),)); # ((3),) it's size of RGB - third dimension.
        
        image_cluster = Image.fromarray(stage);
        
        artist = ax_handle.imshow(image_cluster, interpolation = 'none');
        plt.setp(ax_handle, visible = True);
        
        ax_handle.xaxis.set_ticklabels([]);
        ax_handle.yaxis.set_ticklabels([]);
        ax_handle.xaxis.set_ticks_position('none');
        ax_handle.yaxis.set_ticks_position('none');
        
        return artist;