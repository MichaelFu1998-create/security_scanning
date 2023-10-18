def simulate(self, steps, time, collect_dynamic = False):
        """!
        @brief Performs static simulation of oscillatory network.
        
        @param[in] steps (uint): Number simulation steps.
        @param[in] time (double): Time of simulation.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' is True, than return dynamic for the whole simulation time,
                 otherwise returns only last values (last step of simulation) of output dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        dynamic_amplitude, dynamic_time = ([], []) if collect_dynamic is False else ([self.__amplitude], [0]);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            self.__amplitude = self.__calculate(t, step, int_step);
            
            if collect_dynamic is True:
                dynamic_amplitude.append([ numpy.real(amplitude)[0] for amplitude in self.__amplitude ]);
                dynamic_time.append(t);
        
        if collect_dynamic is False:
            dynamic_amplitude.append([ numpy.real(amplitude)[0] for amplitude in self.__amplitude ]);
            dynamic_time.append(time);

        output_sync_dynamic = fsync_dynamic(dynamic_amplitude, dynamic_time);
        return output_sync_dynamic;