def show_pattern(syncpr_output_dynamic, image_height, image_width):
        """!
        @brief Displays evolution of phase oscillators as set of patterns where the last one means final result of recognition.
        
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        
        """
        number_pictures = len(syncpr_output_dynamic);
        iteration_math_step = 1.0;
        if (number_pictures > 50):
            iteration_math_step = number_pictures / 50.0;
            number_pictures = 50;
        
        number_cols = int(numpy.ceil(number_pictures ** 0.5));
        number_rows = int(numpy.ceil(number_pictures / number_cols));
        
        real_index = 0, 0;
        double_indexer = True;
        if ( (number_cols == 1) or (number_rows == 1) ):
            real_index = 0;
            double_indexer = False;
        
        (_, axarr) = plt.subplots(number_rows, number_cols);
        
        if (number_pictures > 1):
            plt.setp([ax for ax in axarr], visible = False);
            
        iteration_display = 0.0;
        for iteration in range(len(syncpr_output_dynamic)):
            if (iteration >= iteration_display):
                iteration_display += iteration_math_step;
                
                ax_handle = axarr;
                if (number_pictures > 1):
                    ax_handle = axarr[real_index];
                    
                syncpr_visualizer.__show_pattern(ax_handle, syncpr_output_dynamic, image_height, image_width, iteration);
                
                if (double_indexer is True):
                    real_index = real_index[0], real_index[1] + 1;
                    if (real_index[1] >= number_cols):
                        real_index = real_index[0] + 1, 0; 
                else:
                    real_index += 1;
    
        plt.show();