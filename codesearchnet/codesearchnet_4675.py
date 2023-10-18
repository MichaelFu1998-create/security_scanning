def initialize(self, init_type = ema_init_type.KMEANS_INITIALIZATION):
        """!
        @brief Calculates initial parameters for EM algorithm: means and covariances using
                specified strategy.
        
        @param[in] init_type (ema_init_type): Strategy for initialization.
        
        @return (float|list, float|numpy.array) Initial means and variance (covariance matrix in case multi-dimensional data).
        
        """
        if init_type == ema_init_type.KMEANS_INITIALIZATION:
            return self.__initialize_kmeans()
        
        elif init_type == ema_init_type.RANDOM_INITIALIZATION:
            return self.__initialize_random()
        
        raise NameError("Unknown type of EM algorithm initialization is specified.")