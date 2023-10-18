def process(self, steps, time, collect_dynamic=True):
        """!
        @brief Peforms graph coloring analysis using simulation of the oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] collect_dynamic (bool): Specified requirement to collect whole dynamic of the network.
        
        @return (hysteresis_analyser) Returns analyser of results of clustering.
        
        """
        
        output_dynamic = super().simulate(steps, time, collect_dynamic=collect_dynamic)
        return hysteresis_analyser(output_dynamic.output, output_dynamic.time)