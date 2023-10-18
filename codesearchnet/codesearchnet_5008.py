def _calculate_phases(self, solution, t, step, int_step):
        """!
        @brief Calculates new phases for oscillators in the network in line with current step.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states (phases) for oscillators.
        
        """
        
        next_phases = [0.0] * self._num_osc;    # new oscillator _phases
        
        for index in range (0, self._num_osc, 1):
            if (solution == solve_type.FAST):
                result = self._phases[index] + self._phase_kuramoto(self._phases[index], 0, index);
                next_phases[index] = self._phase_normalization(result);
                
            elif ( (solution == solve_type.RK4) or (solution == solve_type.RKF45) ):
                result = odeint(self._phase_kuramoto, self._phases[index], numpy.arange(t - step, t, int_step), (index , ));
                next_phases[index] = self._phase_normalization(result[len(result) - 1][0]);
            
            else:
                raise NameError("Solver '" + str(solution) + "' is not supported");
        
        return next_phases;