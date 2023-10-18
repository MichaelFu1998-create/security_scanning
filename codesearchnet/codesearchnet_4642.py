def __initialize(self, sample):
        """!
        @brief Initializes internal states and resets clustering results in line with input sample.
        
        """
        
        self.__processed = [False] * len(sample)
        self.__optics_objects = [optics_descriptor(i) for i in range(len(sample))]      # List of OPTICS objects that corresponds to objects from input sample.
        self.__ordered_database = []        # List of OPTICS objects in traverse order.
        
        self.__clusters = None      # Result of clustering (list of clusters where each cluster contains indexes of objects from input data).
        self.__noise = None