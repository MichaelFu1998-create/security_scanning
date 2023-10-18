def __alfa_function(self, time, alfa, betta):
        """!
        @brief Calculates value of alfa-function for difference between spike generation time and current simulation time.
        
        @param[in] time (double): Difference between last spike generation time and current time.
        @param[in] alfa (double): Alfa parameter for alfa-function.
        @param[in] betta (double): Betta parameter for alfa-function.
        
        @return (double) Value of alfa-function.
        
        """
        
        return alfa * time * math.exp(-betta * time);