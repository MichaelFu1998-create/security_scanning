def hnn_state(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator.
        
        @param[in] inputs (list): States of oscillator for integration [v, m, h, n] (see description below).
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) new values of oscillator [v, m, h, n], where:
                v - membrane potantial of oscillator,
                m - activation conductance of the sodium channel,
                h - inactication conductance of the sodium channel,
                n - activation conductance of the potassium channel.
        
        """
        
        index = argv;
        
        v = inputs[0]; # membrane potential (v).
        m = inputs[1]; # activation conductance of the sodium channel (m).
        h = inputs[2]; # inactivaton conductance of the sodium channel (h).
        n = inputs[3]; # activation conductance of the potassium channel (n).
        
        # Calculate ion current
        # gNa * m[i]^3 * h * (v[i] - vNa) + gK * n[i]^4 * (v[i] - vK) + gL  (v[i] - vL)
        active_sodium_part = self._params.gNa * (m ** 3) * h * (v - self._params.vNa);
        inactive_sodium_part = self._params.gK * (n ** 4) * (v - self._params.vK);
        active_potassium_part = self._params.gL * (v - self._params.vL);
        
        Iion = active_sodium_part + inactive_sodium_part + active_potassium_part;
        
        Iext = 0.0;
        Isyn = 0.0;
        if (index < self._num_osc): 
            # PN - peripheral neuron - calculation of external current and synaptic current.
            Iext = self._stimulus[index] * self._noise[index];    # probably noise can be pre-defined for reducting compexity
            
            memory_impact1 = 0.0;
            for i in range(0, len(self._central_element[0].pulse_generation_time)):
                memory_impact1 += self.__alfa_function(t - self._central_element[0].pulse_generation_time[i], self._params.alfa_inhibitory, self._params.betta_inhibitory);
            
            memory_impact2 = 0.0;
            for i in range(0, len(self._central_element[1].pulse_generation_time)):
                memory_impact2 += self.__alfa_function(t - self._central_element[1].pulse_generation_time[i], self._params.alfa_inhibitory, self._params.betta_inhibitory);
    
            Isyn = self._params.w2 * (v - self._params.Vsyninh) * memory_impact1 + self._link_weight3[index] * (v - self._params.Vsyninh) * memory_impact2;
        else:
            # CN - central element.
            central_index = index - self._num_osc;
            if (central_index == 0):
                Iext = self._params.Icn1;   # CN1
                
                memory_impact = 0.0;
                for index_oscillator in range(0, self._num_osc):
                    for index_generation in range(0, len(self._pulse_generation_time[index_oscillator])):
                        memory_impact += self.__alfa_function(t - self._pulse_generation_time[index_oscillator][index_generation], self._params.alfa_excitatory, self._params.betta_excitatory);
                 
                Isyn = self._params.w1 * (v - self._params.Vsynexc) * memory_impact;
                
            elif (central_index == 1):
                Iext = self._params.Icn2;   # CN2
                Isyn = 0.0;
                
            else:
                assert 0;
        
        
        # Membrane potential
        dv = -Iion + Iext - Isyn;
        
        # Calculate variables
        potential = v - self._params.vRest;
        am = (2.5 - 0.1 * potential) / (math.exp(2.5 - 0.1 * potential) - 1.0);
        ah = 0.07 * math.exp(-potential / 20.0);
        an = (0.1 - 0.01 * potential) / (math.exp(1.0 - 0.1 * potential) - 1.0);
        
        bm = 4.0 * math.exp(-potential / 18.0);
        bh = 1.0 / (math.exp(3.0 - 0.1 * potential) + 1.0);
        bn = 0.125 * math.exp(-potential / 80.0);
        
        dm = am * (1.0 - m) - bm * m;
        dh = ah * (1.0 - h) - bh * h;
        dn = an * (1.0 - n) - bn * n;
        
        return [dv, dm, dh, dn];