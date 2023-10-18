def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Calculates new state of each oscillator in the network.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Current time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        """
        
        next_excitatory = [0.0] * self._num_osc;
        next_inhibitory = [0.0] * self._num_osc;
        
        next_potential = [];
        if (self._params.ENABLE_POTENTIONAL is True):
            next_potential = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            if (self._params.ENABLE_POTENTIONAL is True):
                result = odeint(self._legion_state, [self._excitatory[index], self._inhibitory[index], self._potential[index]], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index], next_potential[index] ] = result[len(result) - 1][0:3];
                
            else:
                result = odeint(self._legion_state_simplify, [self._excitatory[index], self._inhibitory[index] ], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index] ] = result[len(result) - 1][0:2];
            
            # Update coupling term
            neighbors = self.get_neighbors(index);
            
            coupling = 0
            for index_neighbor in neighbors:
                coupling += self._dynamic_coupling[index][index_neighbor] * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
            
            self._buffer_coupling_term[index] = coupling - self._params.Wz * heaviside(self._global_inhibitor - self._params.teta_xz);
        
        # Update state of global inhibitory
        result = odeint(self._global_inhibitor_state, self._global_inhibitor, numpy.arange(t - step, t, int_step), (None, ));
        self._global_inhibitor = result[len(result) - 1][0];
        
        self._noise = [random.random() * self._params.ro for i in range(self._num_osc)];
        self._coupling_term = self._buffer_coupling_term[:];
        self._inhibitory = next_inhibitory[:];
        self._excitatory = next_excitatory[:];
        
        if (self._params.ENABLE_POTENTIONAL is True):
            self._potential = next_potential[:];