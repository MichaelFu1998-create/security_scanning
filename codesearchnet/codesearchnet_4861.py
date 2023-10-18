def show_second_layer_dynamic(analyser):
        """!
        @brief Shows output dynamic of the second layer.
        
        @param[in] analyser (syncsegm_analyser): Analyser of output dynamic of the 'syncsegm' oscillatory network.
        
        """
        
        second_layer_analysers = analyser.get_second_layer_analysers();
        analysers_sequence = [ object_segment_analyser['analyser'] for object_segment_analyser in second_layer_analysers ]
        
        sync_visualizer.show_output_dynamics(analysers_sequence);