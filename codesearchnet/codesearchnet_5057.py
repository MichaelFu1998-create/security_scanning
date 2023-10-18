def __validate_pattern(self, pattern):
        """!
        @brief Validates pattern.
        @details Throws exception if length of pattern is not equal to size of the network or if it consists feature with value that are not equal to [-1; 1].
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        """
        if (len(pattern) != len(self)):
            raise NameError('syncpr: length of the pattern (' + len(pattern) + ') should be equal to size of the network');
        
        for feature in pattern:
            if ( (feature != -1.0) and (feature != 1.0) ):
                raise NameError('syncpr: patten feature (' + feature + ') should be distributed in [-1; 1]');