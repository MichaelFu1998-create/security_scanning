def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Calculates new states for neurons using differential calculus. Returns new states for neurons.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Current time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states for neurons.
        
        """
        
        next_states = [0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):            
            result = odeint(self._neuron_states, self._states[index], numpy.arange(t - step, t, int_step), (index , ));
            next_states[index] = result[len(result) - 1][0];
        
        self._outputs = [val for val in self._outputs_buffer];
        return next_states;