def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medians algorithm.

        @return (kmedians) Returns itself (K-Medians instance).

        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medians()
        
        """
        
        if self.__ccore is True:
            ccore_metric = metric_wrapper.create_instance(self.__metric)
            self.__clusters, self.__medians = wrapper.kmedians(self.__pointer_data, self.__medians, self.__tolerance, self.__itermax, ccore_metric.get_pointer())

        else:
            changes = float('inf')
             
            # Check for dimension
            if len(self.__pointer_data[0]) != len(self.__medians[0]):
                raise NameError('Dimension of the input data and dimension of the initial medians must be equal.')

            iterations = 0
            while changes > self.__tolerance and iterations < self.__itermax:
                self.__clusters = self.__update_clusters()
                updated_centers = self.__update_medians()
             
                changes = max([self.__metric(self.__medians[index], updated_centers[index]) for index in range(len(updated_centers))])
                 
                self.__medians = updated_centers

                iterations += 1

        return self