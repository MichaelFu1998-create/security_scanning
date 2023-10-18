def get_winner_number(self):
        """!
        @brief Calculates number of winner at the last step of learning process.
        
        @return (uint) Number of winner.
        
        """
        
        if self.__ccore_som_pointer is not None:
            self._award = wrapper.som_get_awards(self.__ccore_som_pointer)
        
        winner_number = 0
        for i in range(self._size):
            if self._award[i] > 0:
                winner_number += 1
                
        return winner_number