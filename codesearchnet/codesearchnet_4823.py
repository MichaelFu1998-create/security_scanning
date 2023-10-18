def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs simulation of the network (performs solving of graph coloring problem).
        
        @param[in] order (double): Defines when process of synchronization in the network is over, range from 0 to 1.
        @param[in] solution (solve_type): defines type (method) of solving diff. equation.
        @param[in] collect_dynamic (bool): If True - return full dynamic of the network, otherwise - last state of phases.
        
        @return (syncnet_analyser) Returns analyser of results of coloring.
        
        """
        
        analyser = self.simulate_dynamic(order, solution, collect_dynamic);
        return syncgcolor_analyser(analyser.output, analyser.time, None);