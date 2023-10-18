def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medoids algorithm.

        @return (kmedoids) Returns itself (K-Medoids instance).

        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medoids()
        
        """
        
        if self.__ccore is True:
            ccore_metric = metric_wrapper.create_instance(self.__metric)
            self.__clusters, self.__medoid_indexes = wrapper.kmedoids(self.__pointer_data, self.__medoid_indexes, self.__tolerance, self.__itermax, ccore_metric.get_pointer(), self.__data_type)
        
        else:
            changes = float('inf')
            iterations = 0

            while changes > self.__tolerance and iterations < self.__itermax:
                self.__clusters = self.__update_clusters()
                update_medoid_indexes = self.__update_medoids()

                changes = max([self.__distance_calculator(self.__medoid_indexes[index], update_medoid_indexes[index]) for index in range(len(update_medoid_indexes))])

                self.__medoid_indexes = update_medoid_indexes

                iterations += 1

        return self