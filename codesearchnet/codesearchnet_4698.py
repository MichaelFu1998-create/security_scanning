def __calculate(self, t, step, int_step):
        """!
        @brief Calculates new amplitudes for oscillators in the network in line with current step.
        
        @param[in] t (double): Time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states (phases) for oscillators.
        
        """
        
        next_amplitudes = [0.0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):
            z = numpy.array(self.__amplitude[index], dtype = numpy.complex128, ndmin = 1);
            result = odeint(self.__calculate_amplitude, z.view(numpy.float64), numpy.arange(t - step, t, int_step), (index , ));
            next_amplitudes[index] = (result[len(result) - 1]).view(numpy.complex128);
        
        return next_amplitudes;