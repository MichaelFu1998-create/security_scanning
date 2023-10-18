def __get_canonical_separate(self, input_separate):
        """!
        @brief Return unified representation of separation value.
        @details It represents list whose size is equal to amount of dynamics, where index of dynamic will show
                  where it should be displayed.

        @param[in] input_separate (bool|list): Input separate representation that should transformed.

        @return (list) Indexes where each dynamic should be displayed.

        """
        if (isinstance(input_separate, list)):
            separate = [0] * len(self.dynamics[0]);
            for canvas_index in range(len(input_separate)):
                dynamic_indexes = input_separate[canvas_index];
                for dynamic_index in dynamic_indexes:
                    separate[dynamic_index] = canvas_index;
            
            return separate;
        
        elif (input_separate is False):
            if (isinstance(self.dynamics[0], list) is True):
                return [ self.canvas ] * len(self.dynamics[0]);
            else:
                return [ self.canvas ];
        
        elif (input_separate is True):
            if (isinstance(self.dynamics[0], list) is True):
                return range(self.canvas, self.canvas + len(self.dynamics[0]));
            else:
                return [ self.canvas ];

        else:
            raise Exception("Incorrect type of argument 'separate' '%s'." % type(input_separate));