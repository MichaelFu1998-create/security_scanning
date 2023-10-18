def allocate_sync_ensembles(self, tolerance = 0.1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """

        if (self.__ccore_legion_dynamic_pointer is not None):
            self.__output = wrapper.legion_dynamic_get_output(self.__ccore_legion_dynamic_pointer);
            
        return allocate_sync_ensembles(self.__output, tolerance);